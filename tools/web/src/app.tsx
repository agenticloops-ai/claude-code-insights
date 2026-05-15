import { useEffect, useMemo, useState } from "preact/hooks";
import type { ParsedDiff } from "diff";
import type { VersionBundle, VersionRow } from "./types.ts";
import { diffBundles } from "./diff.ts";

// In dev (`vite`), data is served by the cci-versions-api middleware under
// /api/*. In prod (`vite build`), the cci-data-emit plugin writes the same
// payloads as static JSON under <BASE>/data/.
const DATA_BASE = import.meta.env.DEV ? "/api" : `${import.meta.env.BASE_URL}data`;

async function fetchVersions(): Promise<VersionRow[]> {
  const url = import.meta.env.DEV ? `${DATA_BASE}/versions` : `${DATA_BASE}/versions.json`;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`failed: ${r.status}`);
  return r.json();
}

async function fetchBundle(dirName: string): Promise<VersionBundle> {
  const url = import.meta.env.DEV
    ? `${DATA_BASE}/v/${encodeURIComponent(dirName)}`
    : `${DATA_BASE}/v/${encodeURIComponent(dirName)}.json`;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`failed: ${r.status}`);
  return r.json();
}

export function App() {
  const [versions, setVersions] = useState<VersionRow[]>([]);
  const [filter, setFilter] = useState("");
  const [fromDir, setFromDir] = useState<string | null>(null);
  const [toDir, setToDir] = useState<string | null>(null);
  const [fromBundle, setFromBundle] = useState<VersionBundle | null>(null);
  const [toBundle, setToBundle] = useState<VersionBundle | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchVersions()
      .then((vs) => {
        setVersions(vs);
        const captured = vs.filter((v) => v.captured);
        if (captured.length >= 2) {
          setFromDir(captured[1].dirName);
          setToDir(captured[0].dirName);
        }
      })
      .catch((e) => setError(String(e)));
  }, []);

  useEffect(() => {
    if (!fromDir) return;
    fetchBundle(fromDir).then(setFromBundle).catch((e) => setError(String(e)));
  }, [fromDir]);
  useEffect(() => {
    if (!toDir) return;
    fetchBundle(toDir).then(setToBundle).catch((e) => setError(String(e)));
  }, [toDir]);

  const filtered = useMemo(() => {
    const f = filter.toLowerCase();
    return versions.filter(
      (v) => v.captured && (!f || v.version.includes(f) || v.date.includes(f) || v.dirName.toLowerCase().includes(f)),
    );
  }, [versions, filter]);

  const capturedCount = useMemo(() => versions.filter((v) => v.captured).length, [versions]);

  const diff = useMemo(() => {
    if (!fromBundle || !toBundle) return null;
    return diffBundles(fromBundle, toBundle);
  }, [fromBundle, toBundle]);

  return (
    <div class="layout">
      <aside class="sidebar">
        <header>
          <h1 class="brand">
            cci<span class="brandDot" aria-hidden="true" />
          </h1>
          <p class="brandSub">claude·code·insights / version delta archive</p>
          <div class="brandStats">
            <span><strong>{capturedCount.toLocaleString()}</strong> captured</span>
            <span class="sep">/</span>
            <span><strong>{versions.length.toLocaleString()}</strong> total releases</span>
          </div>
        </header>
        <div class="searchWrap">
          <input
            type="search"
            placeholder="filter releases…"
            value={filter}
            onInput={(e) => setFilter((e.target as HTMLInputElement).value)}
          />
        </div>
        <ul class="versionList">
          {filtered.map((v) => (
            <li
              key={v.dirName}
              class={`versionRow ${v.dirName === fromDir ? "isFrom" : ""} ${v.dirName === toDir ? "isTo" : ""}`}
              onClick={() => {
                if (!fromDir || (fromDir && toDir)) {
                  setFromDir(v.dirName);
                  setToDir(null);
                  setFromBundle(null);
                  setToBundle(null);
                } else if (fromDir && !toDir && v.dirName !== fromDir) {
                  setToDir(v.dirName);
                }
              }}
            >
              <span class="rowDot" aria-hidden="true" />
              <span class="rowVer">{v.version}</span>
              <span class="rowDate">{v.date}</span>
              <span class="rowMark">
                {v.dirName === fromDir ? "A" : v.dirName === toDir ? "B" : ""}
              </span>
            </li>
          ))}
        </ul>
        <footer>
          <small>click two — A=baseline · B=compare</small>
        </footer>
      </aside>
      <main class="main">
        {error && <div class="error">{error}</div>}
        {!fromBundle || !toBundle ? (
          <div class="empty">
            {fromDir ? "loading bundles…" : "select two versions on the left to open a delta."}
          </div>
        ) : (
          <DiffView from={fromBundle} to={toBundle} diff={diff!} />
        )}
      </main>
    </div>
  );
}

const TAB_LABELS: Record<string, string> = {
  overview: "overview",
  tools: "tools",
  skills: "skills",
  systemPrompt: "system prompt",
  userPrompt: "user prompt",
};

function fmtDelta(n: number, suffix = ""): string {
  if (!n) return "0" + suffix;
  return (n > 0 ? "+" : "") + n.toLocaleString() + suffix;
}

function DiffView(props: { from: VersionBundle; to: VersionBundle; diff: ReturnType<typeof diffBundles> }) {
  const { from, to, diff } = props;
  const [tab, setTab] = useState<"overview" | "tools" | "skills" | "systemPrompt" | "userPrompt">("overview");
  const tabs = ["overview", "tools", "skills", "systemPrompt", "userPrompt"] as const;

  const fromV = from.dirName.split("_").pop() ?? from.dirName;
  const toV = to.dirName.split("_").pop() ?? to.dirName;
  const fromDate = from.dirName.split("_")[0];
  const toDate = to.dirName.split("_")[0];

  const m = (key: string) => diff.metrics.find((x) => x.metric === key);
  const stat = (label: string, metricKey: string, suffix = "") => {
    const row = m(metricKey);
    const cls = row && row.delta > 0 ? "pos" : row && row.delta < 0 ? "neg" : "";
    return (
      <span class="stat" key={metricKey}>
        <em>{label}</em>
        <strong class={cls}>{row ? fmtDelta(row.delta, suffix) : "—"}</strong>
      </span>
    );
  };

  return (
    <>
      <header class="mainHeader">
        <div class="cmdLine">
          <span class="cmdPrompt">$</span>
          <span class="cmdName">cci diff</span>
          <span class="cmdArg from">{fromV}</span>
          <span class="cmdArg arrow">→</span>
          <span class="cmdArg to">{toV}</span>
          <span class="cmdMeta">
            <span>{fromDate}</span>
            <span class="sep">→</span>
            <span>{toDate}</span>
          </span>
        </div>
        <div class="strip">
          {stat("tools", "tools (advertised)")}
          {stat("deferred", "tools (deferred)")}
          {stat("skills", "skills")}
          {stat("sys_prompt", "system_prompt chars", "c")}
          {stat("usr_prompt", "user_prompt chars", "c")}
        </div>
        <nav class="tabs">
          {tabs.map((t, i) => (
            <button
              data-i={String(i + 1).padStart(2, "0")}
              class={tab === t ? "active" : ""}
              onClick={() => setTab(t)}
            >
              {TAB_LABELS[t]}
            </button>
          ))}
        </nav>
      </header>
      {tab === "overview" && <OverviewTab from={from} to={to} diff={diff} />}
      {tab === "tools" && <ToolsTab diff={diff} />}
      {tab === "skills" && <SkillsTab diff={diff} />}
      {tab === "systemPrompt" && <DiffTab patch={diff.systemPromptDiff} />}
      {tab === "userPrompt" && <DiffTab patch={diff.userPromptDiff} />}
    </>
  );
}

function OverviewTab({ from, to, diff }: { from: VersionBundle; to: VersionBundle; diff: ReturnType<typeof diffBundles> }) {
  const fb = from.manifest?.baseline;
  const tb = to.manifest?.baseline;
  return (
    <section class="overview">
      <table class="metricsTable">
        <thead>
          <tr>
            <th>metric</th>
            <th>{from.dirName.split("_").pop()}</th>
            <th>{to.dirName.split("_").pop()}</th>
            <th>Δ</th>
          </tr>
        </thead>
        <tbody>
          {diff.metrics.map((mr) => (
            <tr key={mr.metric}>
              <td>{mr.metric}</td>
              <td>{mr.from.toLocaleString()}</td>
              <td>{mr.to.toLocaleString()}</td>
              <td class={mr.delta > 0 ? "pos" : mr.delta < 0 ? "neg" : ""}>
                {mr.delta ? (mr.delta > 0 ? `+${mr.delta.toLocaleString()}` : mr.delta.toLocaleString()) : ""}
              </td>
            </tr>
          ))}
          <tr>
            <td>models (baseline)</td>
            <td>{(fb?.models ?? []).join(", ")}</td>
            <td>{(tb?.models ?? []).join(", ")}</td>
            <td />
          </tr>
        </tbody>
      </table>
      <details class="releaseNotes">
        <summary>release notes</summary>
        <div class="twoCol">
          <pre>{from.releaseNotes || "—"}</pre>
          <pre>{to.releaseNotes || "—"}</pre>
        </div>
      </details>
    </section>
  );
}

function ToolsTab({ diff }: { diff: ReturnType<typeof diffBundles> }) {
  const t = diff.tools;
  const Group = ({ label, names, kind }: { label: string; names: string[]; kind: string }) =>
    names.length ? (
      <div class={`toolGroup ${kind}`}>
        <h3>
          {label} <span class="muted">{names.length}</span>
        </h3>
        <ul>
          {names.map((n) => (
            <li key={n}>
              <code>{n}</code>
            </li>
          ))}
        </ul>
      </div>
    ) : null;
  return (
    <section class="tools">
      <Group label="added" names={t.added} kind="add" />
      <Group label="removed" names={t.removed} kind="remove" />
      <Group label="moved to deferred" names={t.movedToDeferred} kind="move" />
      <Group label="moved to advertised" names={t.movedToAdvertised} kind="move" />
      <Group label="new deferred" names={t.newDeferred} kind="add" />
      <Group label="removed deferred" names={t.removedDeferred} kind="remove" />
      {t.modified.length > 0 && (
        <div class="toolGroup change">
          <h3>
            modified <span class="muted">{t.modified.length}</span>
          </h3>
          <ul>
            {t.modified.map((mod) => (
              <li key={mod.name}>
                <code>{mod.name}</code>
                <small class="muted">
                  {[mod.descriptionChanged && "desc", mod.schemaChanged && "schema"].filter(Boolean).join(" · ")}
                </small>
              </li>
            ))}
          </ul>
        </div>
      )}
      {t.added.length + t.removed.length + t.movedToDeferred.length + t.movedToAdvertised.length + t.newDeferred.length + t.removedDeferred.length + t.modified.length === 0 && (
        <div class="empty">no tool changes</div>
      )}
    </section>
  );
}

function SkillsTab({ diff }: { diff: ReturnType<typeof diffBundles> }) {
  const s = diff.skills;
  if (s.added.length + s.removed.length + s.descriptionChanged.length === 0) {
    return <div class="empty">no skill changes</div>;
  }
  return (
    <section class="skills">
      {s.added.length > 0 && (
        <div class="toolGroup add">
          <h3>added <span class="muted">{s.added.length}</span></h3>
          <ul>
            {s.added.map((sk) => (
              <li key={sk.name}>
                <code>{sk.name}</code>
                <span class="muted">{sk.description}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {s.removed.length > 0 && (
        <div class="toolGroup remove">
          <h3>removed <span class="muted">{s.removed.length}</span></h3>
          <ul>
            {s.removed.map((sk) => (
              <li key={sk.name}>
                <code>{sk.name}</code>
              </li>
            ))}
          </ul>
        </div>
      )}
      {s.descriptionChanged.length > 0 && (
        <div class="toolGroup change">
          <h3>description changed <span class="muted">{s.descriptionChanged.length}</span></h3>
          <ul>
            {s.descriptionChanged.map((sk) => (
              <li key={sk.name}>
                <code>{sk.name}</code>
                <details>
                  <summary>diff</summary>
                  <div class="twoCol">
                    <pre>{sk.from}</pre>
                    <pre>{sk.to}</pre>
                  </div>
                </details>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

function DiffTab({ patch }: { patch: ParsedDiff }) {
  if (!patch || !patch.hunks || patch.hunks.length === 0) {
    return <div class="empty">no changes</div>;
  }
  return (
    <div class="unifiedDiff">
      {patch.hunks.map((h, hi) => {
        let oldLn = h.oldStart;
        let newLn = h.newStart;
        return (
          <div class="diffBlock" key={hi}>
            <div class="diffHunk">
              @@ -{h.oldStart},{h.oldLines} +{h.newStart},{h.newLines} @@
            </div>
            {h.lines.map((line, li) => {
              const c = line[0] ?? " ";
              const text = line.slice(1);
              let oldStr = "";
              let newStr = "";
              let cls = "diffContext";
              if (c === " ") {
                oldStr = String(oldLn++);
                newStr = String(newLn++);
              } else if (c === "-") {
                oldStr = String(oldLn++);
                cls = "diffRemove";
              } else if (c === "+") {
                newStr = String(newLn++);
                cls = "diffAdd";
              } else if (c === "\\") {
                cls = "diffMeta";
              }
              return (
                <div class={`diffLine ${cls}`} key={li}>
                  <span class="lnOld">{oldStr}</span>
                  <span class="lnNew">{newStr}</span>
                  <span class="lnSign">{c === " " ? "" : c}</span>
                  <span class="lnText">{text}</span>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}
