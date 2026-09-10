import { useEffect, useState } from "react";
import "./Dashboard.css";

// Screen 1 — the single-run dashboard, per 02-prototype-architecture.md §3.
// Real graph + real optimizer results, via the tested /graph, /optimize,
// /runs/{id} endpoints. The AI-explanation section is a placeholder — the
// Ollama integration from 02-ai-role.md is deferred, not built yet.
const API = "http://127.0.0.1:8000";
const METHODS = [
  { key: "random", label: "Random" },
  { key: "centrality", label: "Centrality" },
  { key: "proposed_greedy", label: "Proposed" },
];

// Fixed positions for the 11-node testbed graph — mirrors the zone layout
// in testbed-architecture.md (external → DMZ → supervisory → control).
const LAYOUT = {
  "Attacker": [190, 20], "OT Firewall": [190, 80],
  "DMZ Jump Host": [110, 150], "Historian": [270, 150],
  "Engineering WS": [60, 230], "Engineering WS-2": [160, 230], "HMI": [260, 230],
  "PLC-01": [60, 310], "PLC-02": [160, 310], "PLC-03 (RTU)": [260, 310],
  "Backup Control Switch": [330, 270],
};

function MetricCard({ label, value }) {
  return (
    <div className="metric-card">
      <p className="metric-label">{label}</p>
      <p className="metric-value">{value}</p>
    </div>
  );
}

export default function Dashboard() {
  const [graph, setGraph] = useState(null);
  const [method, setMethod] = useState("proposed_greedy");
  const [run, setRun] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/graph`)
      .then((r) => r.json())
      .then(setGraph)
      .catch((e) => setError(`Can't reach backend: ${e.message}`));
  }, []);

  async function runOptimize() {
    setLoading(true);
    setError(null);
    try {
      const optRes = await fetch(`${API}/optimize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ method, budget: 2 }),
      });
      if (!optRes.ok) throw new Error(`optimize returned ${optRes.status}`);
      const { run_id } = await optRes.json();
      const runRes = await fetch(`${API}/runs/${run_id}`);
      if (!runRes.ok) throw new Error(`runs/${run_id} returned ${runRes.status}`);
      setRun(await runRes.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  if (error) return <div className="dash"><p className="error">{error}</p></div>;
  if (!graph) return <div className="dash"><p>Loading graph…</p></div>;

  const placedIds = new Set((run?.placements ?? []).map((p) => p.asset_id));

  return (
    <div className="dash">
      <div className="toolbar">
        {METHODS.map((m) => (
          <button
            key={m.key}
            className={method === m.key ? "btn btn-active" : "btn"}
            onClick={() => setMethod(m.key)}
          >
            {m.label}
          </button>
        ))}
        <button className="btn btn-run" onClick={runOptimize} disabled={loading}>
          {loading ? "Running…" : "Run"}
        </button>
      </div>

      <div className="dash-grid">
        <div className="panel graph-panel">
          <svg width="100%" viewBox="0 0 400 350" role="img" aria-label="Network graph">
            {graph.edges.map((e, i) => {
              const src = graph.assets.find((a) => a.asset_id === e.source_asset_id);
              const tgt = graph.assets.find((a) => a.asset_id === e.target_asset_id);
              if (!src || !tgt || !LAYOUT[src.name] || !LAYOUT[tgt.name]) return null;
              const [x1, y1] = LAYOUT[src.name];
              const [x2, y2] = LAYOUT[tgt.name];
              return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#d0d0d0" strokeWidth="1" />;
            })}
            {graph.assets.map((a) => {
              const pos = LAYOUT[a.name];
              if (!pos) return null;
              const [x, y] = pos;
              const placed = placedIds.has(a.asset_id);
              return (
                <g key={a.asset_id}>
                  <circle cx={x} cy={y} r={placed ? 12 : 9} fill={placed ? "#1D9E75" : "#b9b9b9"} />
                  <text x={x} y={y + 22} textAnchor="middle" fontSize="9" fill="#555">{a.name}</text>
                </g>
              );
            })}
          </svg>
        </div>

        <div className="panel side-panel">
          {run ? (
            <>
              <div className="metrics-grid">
                <MetricCard label="Coverage" value={`${Math.round(run.coverage_score * 100)}%`} />
                <MetricCard label="Early" value={run.early_score.toFixed(2)} />
                <MetricCard label="CritProt" value={`${Math.round(run.critprot_score * 100)}%`} />
                <MetricCard label="Cost" value={run.cost_score} />
              </div>
              <div className="panel explain-panel">
                <p className="explain-label">AI explanation</p>
                <p className="explain-placeholder">
                  Not wired yet — needs the Ollama integration from 02-ai-role.md.
                </p>
              </div>
            </>
          ) : (
            <p className="hint">Pick a method and hit Run.</p>
          )}
        </div>
      </div>
    </div>
  );
}
