import { useEffect, useMemo, useState } from "preact/hooks";
import type { VersionBundle, VersionRow } from "./types.ts";
import { diffBundles } from "./diff.ts";

async function fetchVersions(): Promise<VersionRow[]> {
  const r = await fetch("/api/versions");
  return r.json();
}

async function fetchBundle(dirName: string): Promise<VersionBundle> {
  const r = await fetch(`/api/v/${encodeURIComponent(dirName)}`);
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
          setFromDir(captured[captured.length - 2].dirName);
          setToDir(captured[captured.length - 1].dirName);
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

  const diff = useMemo(() => {
    if (!fromBundle || !toBundle) return null;
    return diffBundles(fromBundle, toBundle);
  }, [fromBundle, toBundle]);

  return (
    <div class="layout">
      <aside class="sidebar">
        <header>
          <h1>cci</h1>
          <p class="muted">claude-code-insights</p>
        </header>
        <input type="search" placeholder="filter…" value={filter} onInput={(e) => setFilter((e.target as HTMLInputElement).value)} />
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
              <span class="rowVer">{v.version}</span>
              <span class="rowDate">{v.date}</span>
              <span class="rowMark">
                {v.dirName === fromDir ? "A" : v.dirName === toDir ? "B" : ""}
              </span>
            </li>
          ))}
        </ul>
        <footer>
          <small>click two: A=from, B=to</small>
        </footer>
      </aside>
      <main class="main">
        {error && <div class="error">{error}</div>}
        {!fromBundle || !toBundle ? (
          <div class="empty">{fromDir ? "loading bundles…" : "pick two versions on the left"}</div>
        ) : (
          <DiffView from={fromBundle} to={toBundle} diff={diff!} />
        )}
      </main>
    </div>
  );
}

function DiffView(props: { from: VersionBundle; to: VersionBundle; diff: ReturnType<typeof diffBundles> }) {
  const { from, to, diff } = props;
  const [tab, setTab] = useState<"overview" | "tools" | "skills" | "systemPrompt" | "userPrompt">("overview");
  return (
    <>
      <header class="mainHeader">
        <h2>
          {from.dirName} <span class="arrow">→</span> {to.dirName}
        </h2>
        <nav class="tabs">
          {(["overview", "tools", "skills", "systemPrompt", "userPrompt"] as const).map((t) => (
            <button class={tab === t ? "active" : ""} onClick={() => setTab(t)}>
              {t}
            </button>
          ))}
        </nav>
      </header>
      {tab === "overview" && <OverviewTab from={from} to={to} diff={diff} />}
      {tab === "tools" && <ToolsTab diff={diff} />}
      {tab === "skills" && <SkillsTab diff={diff} />}
      {tab === "systemPrompt" && <DiffTab patch={diff.systemPromptUnified} />}
      {tab === "userPrompt" && <DiffTab patch={diff.userPromptUnified} />}
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
          {diff.metrics.map((m) => (
            <tr key={m.metric}>
              <td>{m.metric}</td>
              <td>{m.from}</td>
              <td>{m.to}</td>
              <td class={m.delta > 0 ? "pos" : m.delta < 0 ? "neg" : ""}>
                {m.delta > 0 ? `+${m.delta}` : m.delta || ""}
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
          {label} <span class="muted">({names.length})</span>
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
            modified <span class="muted">({t.modified.length})</span>
          </h3>
          <ul>
            {t.modified.map((m) => (
              <li key={m.name}>
                <code>{m.name}</code>{" "}
                <small class="muted">
                  {[m.descriptionChanged && "desc", m.schemaChanged && "schema"].filter(Boolean).join(", ")}
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
          <h3>added ({s.added.length})</h3>
          <ul>
            {s.added.map((sk) => (
              <li key={sk.name}>
                <code>{sk.name}</code>: <span class="muted">{sk.description}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {s.removed.length > 0 && (
        <div class="toolGroup remove">
          <h3>removed ({s.removed.length})</h3>
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
          <h3>description changed ({s.descriptionChanged.length})</h3>
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

function DiffTab({ patch }: { patch: string }) {
  if (!patch || patch.split("\n").length < 5) return <div class="empty">no changes</div>;
  return (
    <pre class="unifiedDiff">
      {patch.split("\n").map((line, i) => {
        let cls = "";
        if (line.startsWith("+++") || line.startsWith("---")) cls = "diffHeader";
        else if (line.startsWith("@@")) cls = "diffHunk";
        else if (line.startsWith("+")) cls = "diffAdd";
        else if (line.startsWith("-")) cls = "diffRemove";
        return (
          <div key={i} class={cls}>
            {line}
          </div>
        );
      })}
    </pre>
  );
}
