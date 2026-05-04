#!/usr/bin/env python3
"""Batch-capture every changelog-documented claude-code version, one at a time.

For each version (oldest first):
    build → run all scenarios → extract → summarize → fetch-notes → prune image

A version is marked "failed" and its directory deleted when 02-bare doesn't
produce extracted artifacts (agent-mode timeouts, auth issues, etc.). Versions
where 02-bare succeeds but other scenarios time-out are kept as partial captures.

After all versions are processed, a sequential diff pass generates
diff-from-<prev>.md for every consecutive pair of surviving versions.

Status is appended to versions/.batch-status.jsonl (one JSON line per version)
so reruns and monitoring work.

Usage:
    scripts/batch-capture.py                       # full run (all documented versions)
    scripts/batch-capture.py --skip-existing       # skip versions already captured
    scripts/batch-capture.py --no-diff             # skip the diff pass
    scripts/batch-capture.py --keep-images         # don't prune cch:<v> images
    scripts/batch-capture.py --scenario-timeout 60 # stricter timeout per scenario
    scripts/batch-capture.py --versions LIST_FILE  # one version per line
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_DIR / "scripts"
SANDBOX_DIR = REPO_DIR / "sandbox"
VERSIONS_DIR = REPO_DIR / "versions"
STATUS_FILE = VERSIONS_DIR / ".batch-status.jsonl"

sys.path.insert(0, str(SCRIPTS_DIR))
from _paths import dir_for, find_existing_dir  # noqa: E402


# ---------------------------------------------------------------------------
# Subprocess helper
# ---------------------------------------------------------------------------

def _run(cmd: list[str], *, env: dict | None = None,
         capture_output: bool = False) -> tuple[int, str, str]:
    merged_env = {**os.environ, **(env or {})}
    result = subprocess.run(
        cmd,
        env=merged_env,
        capture_output=capture_output,
        text=True,
    )
    return result.returncode, result.stdout or "", result.stderr or ""


# ---------------------------------------------------------------------------
# Status registry
# ---------------------------------------------------------------------------

def _append_status(row: dict) -> None:
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATUS_FILE, "a") as f:
        f.write(json.dumps(row) + "\n")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Version list
# ---------------------------------------------------------------------------

def _load_versions(args) -> list[str]:
    if args.versions:
        lines = Path(args.versions).read_text().splitlines()
        return [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]
    rc, stdout, _ = _run(
        [sys.executable, str(SCRIPTS_DIR / "list-versions.py")],
        capture_output=True,
    )
    if rc != 0:
        sys.exit("Failed to fetch version list from list-versions.py")
    return [v.strip() for v in stdout.splitlines() if v.strip()]


def _version_already_captured(version: str) -> bool:
    existing = find_existing_dir(version)
    return bool(existing and (existing / "manifest.json").exists())


# ---------------------------------------------------------------------------
# Git commit helper
# ---------------------------------------------------------------------------

def _git_commit_version(version: str, dir_name: str) -> bool:
    version_dir = VERSIONS_DIR / dir_name
    print(f"[{version}] committing …", flush=True)
    rc, _, err = _run(
        ["git", "add", str(version_dir), str(STATUS_FILE)],
        capture_output=True,
    )
    if rc != 0:
        print(f"[{version}]   git add failed: {err[:200]}", flush=True)
        return False
    msg = (
        f"Capture: {version}\n\n"
        "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    )
    rc, out, err = _run(["git", "commit", "-m", msg], capture_output=True)
    if rc == 0:
        print(f"[{version}]   {out.splitlines()[0] if out else 'committed'}", flush=True)
        return True
    print(f"[{version}]   git commit failed: {err[:200]}", flush=True)
    return False


# ---------------------------------------------------------------------------
# Per-version pipeline
# ---------------------------------------------------------------------------

def _process_version(version: str, scenario_timeout: int,
                     keep_images: bool, prev_version: str | None = None,
                     no_diff: bool = False) -> dict:
    started_at = _now()
    print(f"\n{'='*60}", flush=True)
    print(f"[{version}] starting", flush=True)

    # Resolve the versions directory name.
    try:
        dir_name = dir_for(version)
    except SystemExit as e:
        print(f"[{version}] SKIP — cannot resolve dir: {e}", flush=True)
        return {"version": version, "started_at": started_at,
                "finished_at": _now(), "skipped": True, "reason": str(e)}

    version_dir = VERSIONS_DIR / dir_name

    # Build image.
    print(f"[{version}] building image …", flush=True)
    rc, _, err = _run(["bash", str(SANDBOX_DIR / "build.sh"), version])
    if rc != 0:
        print(f"[{version}] BUILD FAILED", flush=True)
        return _failed_row(version, dir_name, started_at,
                           reason=f"build failed: {err[:200]}")

    # Run every scenario.
    scenario_names = sorted(
        p.name for p in (REPO_DIR / "scenarios").iterdir()
        if p.is_dir() and p.name != "README.md"
    )

    scenario_results: dict[str, dict] = {}
    env = {"CAPTURE_TIMEOUT_SECS": str(scenario_timeout) if scenario_timeout else "0"}

    for scen in scenario_names:
        s_start = time.monotonic()
        print(f"[{version}]   {scen} …", flush=True)
        rc, _, _ = _run(
            ["bash", str(SCRIPTS_DIR / "run-scenario.sh"), version, scen],
            env=env,
        )
        duration = round(time.monotonic() - s_start, 1)
        timed_out = (rc == 124)
        skipped = (rc == 125)
        scenario_results[scen] = {
            "exit": rc, "duration_s": duration,
            "timeout": timed_out, "skipped": skipped,
        }
        if skipped:
            tag = "SKIP"
        elif timed_out:
            tag = "TIMEOUT"
        elif rc == 0:
            tag = "OK"
        else:
            tag = f"FAIL({rc})"
        print(f"[{version}]   {scen} → {tag} ({duration}s)", flush=True)

        # If 02-bare hard-failed (not skipped, not timed out), skip remaining
        # agent scenarios — the version likely has auth incompatibility.
        if scen == "02-bare" and rc != 0 and not timed_out and not skipped:
            print(f"[{version}]   02-bare failed — skipping remaining scenarios", flush=True)
            break

    # Extract every fresh agent-mode capture.
    print(f"[{version}] extracting …", flush=True)
    for scen in scenario_names:
        scen_dir = version_dir / "scenarios" / scen
        if not (scen_dir / "raw").exists():
            continue
        rc, _, _ = _run(
            [sys.executable, str(SCRIPTS_DIR / "extract.py"), str(scen_dir)],
            capture_output=True,
        )
        scenario_results[scen]["extract_ok"] = (rc == 0)
        if rc != 0:
            print(f"[{version}]   extract failed for {scen} (non-fatal)", flush=True)

    # Check 02-bare extraction. If the extract.py wrote a stub stats.json with
    # an "error" field, the agent never sent a request — keep the dir so the
    # captured cli-help scenario is still useful, but skip the
    # downstream summarize step (it requires baseline artifacts).
    bare_stats = version_dir / "scenarios" / "02-bare" / "stats.json"
    bare_usable = False
    if bare_stats.exists():
        try:
            bare_usable = "error" not in json.loads(bare_stats.read_text())
        except Exception:
            bare_usable = False

    if not bare_usable:
        reason = "02-bare extract missing" if not bare_stats.exists() else "02-bare captured no requests"
        print(f"[{version}] PARTIAL — {reason}; keeping dir, skipping summarize", flush=True)
        _prune_image(version, keep_images)
        row = _failed_row(version, dir_name, started_at,
                          reason=reason, deleted=False,
                          scenarios=scenario_results)
        _append_status(row)
        return row

    # Summarize.
    print(f"[{version}] summarizing …", flush=True)
    rc, _, err = _run(
        [sys.executable, str(SCRIPTS_DIR / "summarize-version.py"), version],
        capture_output=True,
    )
    summarize_ok = rc == 0
    if not summarize_ok:
        print(f"[{version}]   summarize failed (non-fatal): {err[:200]}", flush=True)

    # Fetch release notes.
    print(f"[{version}] fetching release notes …", flush=True)
    rc, _, _ = _run(
        [sys.executable, str(SCRIPTS_DIR / "fetch-release-notes.py"), version],
        capture_output=True,
    )
    release_notes_ok = rc == 0

    # Diff against previous successful version (inline, before commit).
    diff_ok = False
    if prev_version and not no_diff:
        print(f"[{version}] diffing from {prev_version} …", flush=True)
        rc, _, err = _run(
            [sys.executable, str(SCRIPTS_DIR / "diff-versions.py"), prev_version, version],
            capture_output=True,
        )
        diff_ok = rc == 0
        if not diff_ok:
            print(f"[{version}]   diff failed (non-fatal): {err[:200]}", flush=True)

    # Prune image.
    _prune_image(version, keep_images)

    finished_at = _now()
    print(f"[{version}] DONE — summarize={'ok' if summarize_ok else 'fail'}", flush=True)

    row = {
        "version": version,
        "dir_name": dir_name,
        "started_at": started_at,
        "finished_at": finished_at,
        "scenarios": scenario_results,
        "summarize_ok": summarize_ok,
        "release_notes_ok": release_notes_ok,
        "diff_ok": diff_ok,
        "deleted": False,
        "image_pruned": not keep_images,
    }
    _append_status(row)
    _git_commit_version(version, dir_name)
    return row


def _prune_image(version: str, keep_images: bool) -> None:
    if keep_images:
        return
    print(f"[{version}] pruning image …", flush=True)
    _run(["docker", "rmi", f"cch:{version}"], capture_output=True)


def _failed_row(version: str, dir_name: str, started_at: str, *,
                reason: str, deleted: bool = False,
                scenarios: dict | None = None) -> dict:
    return {
        "version": version,
        "dir_name": dir_name,
        "started_at": started_at,
        "finished_at": _now(),
        "scenarios": scenarios or {},
        "summarize_ok": False,
        "release_notes_ok": False,
        "deleted": deleted,
        "image_pruned": True,
        "failure_reason": reason,
    }


# ---------------------------------------------------------------------------
# Diff pass
# ---------------------------------------------------------------------------

def _run_diffs() -> None:
    print("\n[diff] starting diff pass …", flush=True)
    surviving = sorted(
        d for d in VERSIONS_DIR.iterdir()
        if d.is_dir() and (d / "manifest.json").exists()
    )
    if len(surviving) < 2:
        print("[diff] fewer than 2 surviving versions — skipping", flush=True)
        return

    prev = None
    ok = fail = skip = 0
    for vdir in surviving:
        if prev is None:
            prev = vdir
            continue
        prev_v = prev.name.split("_", 1)[1] if "_" in prev.name else prev.name
        curr_v = vdir.name.split("_", 1)[1] if "_" in vdir.name else vdir.name
        # Skip if the diff file already exists (written inline during capture).
        if list(vdir.glob(f"diff-from-{prev_v}.md")):
            skip += 1
            prev = vdir
            continue
        print(f"[diff] {prev_v} → {curr_v} …", flush=True)
        rc, _, err = _run(
            [sys.executable, str(SCRIPTS_DIR / "diff-versions.py"), prev_v, curr_v],
            capture_output=True,
        )
        if rc == 0:
            ok += 1
        else:
            print(f"[diff]   failed (non-fatal): {err[:200]}", flush=True)
            fail += 1
        prev = vdir
    print(f"[diff] done: {ok} ok, {fail} failed, {skip} already present", flush=True)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _write_summary(results: list[dict]) -> None:
    passed = [r for r in results if r.get("summarize_ok")]
    failed = [r for r in results if not r.get("summarize_ok") and not r.get("skipped")]
    skipped = [r for r in results if r.get("skipped")]

    lines = [
        "# Batch capture summary",
        "",
        f"- Total processed: {len(results)}",
        f"- Succeeded: {len(passed)}",
        f"- Failed/deleted: {len(failed)}",
        f"- Skipped: {len(skipped)}",
        "",
        "## Failed versions",
        "",
    ]
    for r in failed:
        lines.append(f"- `{r['version']}`: {r.get('failure_reason', 'unknown')}")
    if not failed:
        lines.append("(none)")

    lines += ["", "## Succeeded versions", ""]
    for r in passed:
        scen_ok = sum(1 for s in r.get("scenarios", {}).values() if s.get("exit") == 0)
        scen_total = len(r.get("scenarios", {}))
        lines.append(f"- `{r['version']}` ({scen_ok}/{scen_total} scenarios ok)")

    out = VERSIONS_DIR / ".batch-status.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"\n[main] summary → {out.relative_to(REPO_DIR)}", flush=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scenario-timeout", type=int, default=300,
                        help="per-scenario timeout in seconds (default: 300, 0=none)")
    parser.add_argument("--versions",
                        help="file with one version per line (default: all documented)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="skip versions that already have manifest.json")
    parser.add_argument("--no-diff", action="store_true",
                        help="skip the diff pass after all captures")
    parser.add_argument("--keep-images", action="store_true",
                        help="don't prune cch:<version> images after capture")
    parser.add_argument("--reverse", action="store_true",
                        help="process versions newest-first (default: oldest-first)")
    parser.add_argument("--stop-after-failures", type=int, default=0,
                        help="stop after N consecutive 02-bare failures (0=never stop)")
    args = parser.parse_args()

    versions = _load_versions(args)
    if args.skip_existing:
        versions = [v for v in versions if not _version_already_captured(v)]
    if args.reverse:
        versions = list(reversed(versions))

    print(f"[main] {len(versions)} versions to process (sequential, {'newest' if args.reverse else 'oldest'}-first)", flush=True)
    if not versions:
        print("[main] nothing to do.", flush=True)
        return 0

    results = []
    consecutive_failures = 0
    last_good_version: str | None = None
    for i, v in enumerate(versions, 1):
        print(f"\n[main] progress: {i}/{len(versions)}", flush=True)
        row = _process_version(
            v, args.scenario_timeout, args.keep_images,
            prev_version=last_good_version,
            no_diff=args.no_diff,
        )
        results.append(row)

        if row.get("summarize_ok"):
            last_good_version = v

        if row.get("deleted"):
            consecutive_failures += 1
        else:
            consecutive_failures = 0

        if args.stop_after_failures and consecutive_failures >= args.stop_after_failures:
            print(f"\n[main] {consecutive_failures} consecutive failures — stopping early", flush=True)
            break

    if not args.no_diff:
        _run_diffs()

    _write_summary(results)

    passed = sum(1 for r in results if r.get("summarize_ok"))
    print(f"\n[main] DONE — {passed}/{len(results)} passed", flush=True)
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
