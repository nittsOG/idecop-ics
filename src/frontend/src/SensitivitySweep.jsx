import { useEffect, useState } from "react";
import "./SensitivitySweep.css";

// Screen 2 — the sensitivity-sweep comparison (02-prototype-architecture.md §3; D46).
// For one budget and every weighting of the declared grid (scripts/sweep.py), it reads
// GET /runs/compare: the latest stored run of each deterministic method, and the mean of
// the 30 random placements, computed on request because a stored random run is one trial
// (D17). The charts draw the proposed method against its two baselines; the table holds
// every method, distorted greedy and the MILP included. It changes no input: the sweep
// button only asks POST /optimize for runs, as the Dashboard does.
const API = "http://127.0.0.1:8000";
const SWEEP_METHODS = ["proposed_greedy", "proposed_distorted_greedy", "proposed_milp", "centrality"];
const SERIES = [
  { key: "proposed_greedy", label: "Proposed (greedy)", color: "var(--series-1)" },
  { key: "centrality", label: "Centrality", color: "var(--series-2)" },
  { key: "random", label: "Random (mean of 30)", color: "var(--series-3)" },
];
const METRICS = [
  { key: "objective_value", label: "F, the objective", note: "higher is better" },
  { key: "coverage_score", label: "Coverage", note: "higher is better" },
  { key: "early_score", label: "Early detection", note: "higher is better" },
  { key: "critprot_score", label: "Critical-asset protection", note: "higher is better" },
  { key: "risk_score", label: "Detectability risk", note: "a penalty: lower is better" },
  { key: "cost_score", label: "Cost", note: "a penalty: lower is better" },
];
const METHOD_LABEL = {
  proposed_greedy: "Proposed (greedy)",
  proposed_distorted_greedy: "Distorted greedy",
  proposed_milp: "MILP (exact)",
  centrality: "Centrality",
  random: "Random (mean of 30)",
};
const GREEK = { alpha: "α", beta: "β", gamma: "γ", delta: "δ", epsilon: "ε" };
const weightingLabel = (name) => name.replace(/^(alpha|beta|gamma|delta|epsilon)=/, (_, g) => `${GREEK[g]} = `);
const four = (v) => (v == null ? "not run" : v.toFixed(4));

// Clean axis ticks: about four intervals of 1, 2, 2.5 or 5 times a power of ten.
function niceScale(lo, hi) {
  if (hi - lo < 1e-12) hi = lo + 1;
  const raw = (hi - lo) / 4;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((f) => f * mag).find((s) => s >= raw);
  const start = Math.floor(lo / step + 1e-9) * step;
  const end = Math.ceil(hi / step - 1e-9) * step;
  const ticks = [];
  for (let t = start; t <= end + step / 2; t += step) ticks.push(Math.abs(t) < 1e-12 ? 0 : t);
  const decimals = Math.max(0, -Math.floor(Math.log10(step) + 1e-9) + (step / mag === 2.5 ? 1 : 0));
  return { lo: start, hi: end, ticks, decimals };
}

// A column grows from the zero line; only its data end is rounded (4 px).
function columnPath(x, w, y0, y1) {
  const h = Math.abs(y1 - y0);
  if (h < 0.5) return null;
  const r = Math.min(4, h, w / 2);
  if (y1 < y0) {
    return `M${x},${y0} V${y1 + r} Q${x},${y1} ${x + r},${y1} H${x + w - r} Q${x + w},${y1} ${x + w},${y1 + r} V${y0} Z`;
  }
  return `M${x},${y0} V${y1 - r} Q${x},${y1} ${x + r},${y1} H${x + w - r} Q${x + w},${y1} ${x + w},${y1 - r} V${y0} Z`;
}

async function fetchCompare(budget) {
  let res;
  try {
    res = await fetch(`${API}/runs/compare?budget=${budget}`);
  } catch (e) {
    throw new Error(`Can't reach backend: ${e.message}`);
  }
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail ?? `The backend returned ${res.status}.`);
  return body;
}

function SmallMultiple({ metric, weightings, valueOf, budget }) {
  const [active, setActive] = useState(null);
  const W = 520, H = 210, m = { top: 10, right: 8, bottom: 28, left: 44 };
  const pw = W - m.left - m.right, ph = H - m.top - m.bottom;
  const values = weightings.flatMap((w) => SERIES.map((s) => valueOf(w.name, s.key, metric.key))).filter((v) => v != null);
  const scale = niceScale(Math.min(0, ...values), Math.max(0, ...values));
  const y = (v) => m.top + ph - ((v - scale.lo) / (scale.hi - scale.lo)) * ph;
  const band = pw / weightings.length;
  const gap = 2;
  const barW = Math.min(24, (band - 20 - gap * (SERIES.length - 1)) / SERIES.length);
  const groupW = SERIES.length * barW + gap * (SERIES.length - 1);
  const describe = (w) =>
    `${weightingLabel(w.name)}: ` + SERIES.map((s) => `${s.label} ${four(valueOf(w.name, s.key, metric.key))}`).join(", ");

  return (
    <figure className="sm">
      <figcaption>
        <span className="sm-title">{metric.label}</span>
        <span className="sm-note">{metric.note}</span>
      </figcaption>
      <div className="sm-plot">
        <svg viewBox={`0 0 ${W} ${H}`} role="img"
             aria-label={`${metric.label} at B = ${budget}, by weighting. Every value is also in the table below.`}>
          {active != null && (
            <rect className="hover-band" x={m.left + active * band} y={m.top} width={band} height={ph} rx="4" />
          )}
          {scale.ticks.map((t) => (
            <g key={t}>
              <line className={t === 0 ? "axis" : "grid"} x1={m.left} x2={W - m.right} y1={y(t)} y2={y(t)} />
              <text className="tick" x={m.left - 6} y={y(t)} textAnchor="end" dominantBaseline="middle">
                {t.toFixed(scale.decimals)}
              </text>
            </g>
          ))}
          {weightings.map((w, i) => {
            const x0 = m.left + i * band + (band - groupW) / 2;
            return (
              <g key={w.name}>
                {SERIES.map((s, j) => {
                  const v = valueOf(w.name, s.key, metric.key);
                  const d = v == null ? null : columnPath(x0 + j * (barW + gap), barW, y(0), y(v));
                  return d && <path key={s.key} d={d} fill={s.color} />;
                })}
                <text className="tick" x={m.left + i * band + band / 2} y={H - 8} textAnchor="middle">
                  {weightingLabel(w.name)}
                </text>
                <rect className="hit" x={m.left + i * band} y={m.top} width={band} height={ph} tabIndex={0}
                      aria-label={describe(w)}
                      onMouseEnter={() => setActive(i)} onMouseLeave={() => setActive(null)}
                      onFocus={() => setActive(i)} onBlur={() => setActive(null)} />
              </g>
            );
          })}
        </svg>
        {active != null && (
          <div className={`tip${active === 0 ? " tip-left" : active === weightings.length - 1 ? " tip-right" : ""}`}
               style={{ left: `${((m.left + active * band + band / 2) / W) * 100}%` }}>
            <p className="tip-head">{weightingLabel(weightings[active].name)}</p>
            {SERIES.map((s) => (
              <p className="tip-row" key={s.key}>
                <svg width="14" height="8" aria-hidden="true">
                  <line x1="1" x2="13" y1="4" y2="4" stroke={s.color} strokeWidth="2" strokeLinecap="round" />
                </svg>
                <strong>{four(valueOf(weightings[active].name, s.key, metric.key))}</strong>
                <span>{s.label}</span>
              </p>
            ))}
          </div>
        )}
      </div>
    </figure>
  );
}

export default function SensitivitySweep() {
  const [budget, setBudget] = useState(2);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(true);
  const [running, setRunning] = useState(null);

  // The effect sets state only in the promise's callbacks; the event that changes the budget
  // marks the view as refreshing. A reply for a budget no longer shown is dropped.
  useEffect(() => {
    let current = true;
    fetchCompare(budget)
      .then((body) => {
        if (current) {
          setData(body);
          setError(null);
        }
      })
      .catch((e) => current && setError(e.message))
      .finally(() => current && setRefreshing(false));
    return () => {
      current = false;
    };
  }, [budget]);

  function pickBudget(b) {
    if (b === budget) return;
    setRefreshing(true);
    setBudget(b);
  }

  async function runSweep() {
    const total = data.weightings.length * SWEEP_METHODS.length;
    setRunning({ done: 0, total });
    setError(null);
    try {
      for (const w of data.weightings) {
        for (const method of SWEEP_METHODS) {
          const res = await fetch(`${API}/optimize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ method, budget, alpha: w.alpha, beta: w.beta, gamma: w.gamma, delta: w.delta, epsilon: w.epsilon }),
          });
          if (!res.ok) {
            const body = await res.json().catch(() => ({}));
            throw new Error(body.detail ?? `optimize returned ${res.status}`);
          }
          setRunning((r) => ({ ...r, done: r.done + 1 }));
        }
      }
      setRefreshing(true);
      setData(await fetchCompare(budget));
    } catch (e) {
      setError(e.message);
    } finally {
      setRunning(null);
      setRefreshing(false);
    }
  }

  const rowOf = (weighting, method) => data?.rows.find((r) => r.weighting === weighting && r.method === method);
  const valueOf = (weighting, method, key) => rowOf(weighting, method)?.[key] ?? null;
  const budgets = data?.budgets ?? [1, 2, 3, 4];
  // While a new budget loads, the previous render stays, faded, and is labelled with its own budget.
  const showData = data;
  const missing = showData?.missing.length ?? 0;
  const milpAgrees = showData && !missing
    ? showData.weightings.filter((w) => Math.abs(valueOf(w.name, "proposed_milp", "objective_value")
        - valueOf(w.name, "proposed_greedy", "objective_value")) <= 1e-9).length
    : null;

  return (
    <div className="sweep">
      <h2>Sensitivity sweep</h2>
      <p className="lede">
        How each method's scores move across the five declared weightings of the objective, at one budget.
        α weights coverage, β early detection, γ critical-asset protection and δ detectability risk; ε, the
        cost weight, stays 0.1.
      </p>

      <div className="filters">
        <span className="filter-label">Budget</span>
        {budgets.map((b) => (
          <button key={b} className={b === budget ? "sbtn sbtn-on" : "sbtn"} onClick={() => pickBudget(b)}
                  disabled={running != null} aria-pressed={b === budget}>
            B = {b}
          </button>
        ))}
        <button className="sbtn sbtn-run" onClick={runSweep} disabled={!data || running != null || refreshing}>
          {running ? `Running ${running.done} of ${running.total}…` : `Run the sweep at B = ${budget}`}
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      {!showData && !error && <p className="hint">Loading…</p>}

      {showData && (
        <div className={refreshing ? "sweep-body is-refreshing" : "sweep-body"}>
          <p className="status">
            {missing
              ? `${missing} of ${showData.weightings.length * SWEEP_METHODS.length} runs at B = ${showData.budget} are not stored yet. Run the sweep to make them; until then their columns are left out.`
              : `Each column is the latest stored run of that method and weighting at B = ${showData.budget}.`}
            {milpAgrees != null &&
              ` The MILP's F equals greedy's in ${milpAgrees} of ${showData.weightings.length} weightings.`}
          </p>

          <div className="legend" aria-label="Legend">
            {SERIES.map((s) => (
              <span className="legend-item" key={s.key}>
                <svg width="12" height="12" aria-hidden="true"><rect width="12" height="12" rx="2" fill={s.color} /></svg>
                {s.label}
              </span>
            ))}
            <span className="legend-order">left to right in each group</span>
          </div>
          <p className="note">
            Random is the mean of 30 random placements (seed 42), computed on request: a stored random run is one
            trial (D17). Distorted greedy and the MILP are in the table.
          </p>

          <div className="sm-grid">
            {METRICS.map((metric) => (
              <SmallMultiple key={metric.key} metric={metric} weightings={showData.weightings}
                             valueOf={valueOf} budget={showData.budget} />
            ))}
          </div>

          <h3>Every value at B = {showData.budget}</h3>
          <div className="table-wrap">
            <table className="sweep-table">
              <thead>
                <tr>
                  <th>Weighting</th><th>Method</th><th>Placement</th>
                  <th className="num">F</th><th className="num">Coverage</th><th className="num">Early</th>
                  <th className="num">CritProt</th><th className="num">Risk</th><th className="num">Cost</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {showData.weightings.flatMap((w) =>
                  showData.methods.map((method, j) => {
                    const r = rowOf(w.name, method);
                    return (
                      <tr key={`${w.name}-${method}`} className={j === 0 ? "group-start" : undefined}>
                        <td>{j === 0 ? weightingLabel(w.name) : ""}</td>
                        <td>{METHOD_LABEL[method]}</td>
                        <td>{r ? (r.placement ? r.placement.join(", ") : "30 random placements") : "—"}</td>
                        {METRICS.map((metric) => (
                          <td className="num" key={metric.key}>{four(r?.[metric.key])}</td>
                        ))}
                        <td>{r ? (r.run_id != null ? `run ${r.run_id}` : "computed") : "not run"}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
