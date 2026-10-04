import { useEffect, useState } from "react";
import "./App.css";

// Screen 3 — plausibility review (Filter 1, formal-problem-definition.md §4).
// D26: route A (the AI's answers pre-fill each card, you confirm or change them)
// with three safeguards:
// - three blind cards that you score before seeing any AI answer;
// - a written reason wherever an answer decides the outcome;
// - no silent fallback to the AI's answer.
// The rules mirror src/plausibility; the API enforces them, so a mismatch here
// shows up as an error message, never as a wrong score.
const API = "http://127.0.0.1:8000";

const CRITERIA = [
  ["decoy_exists", "Feasibility", "Can a convincing decoy of this asset type exist at this position?"],
  ["attacker_reach", "Interaction", "Would an attacker on the listed paths interact with it?"],
  ["useful_signal", "Intelligence yield", "Would the interaction tell you something useful?"],
  ["reliable_indicator", "Malice fidelity", "Is a touch reliably an attacker, not routine benign activity?"],
];
const LEVELS = [
  ["yes", "Yes"],
  ["mostly_yes", "Mostly Yes"],
  ["mostly_no", "Mostly No"],
  ["no", "No"],
];
const LABEL = Object.fromEntries(LEVELS);
const BOUNDARY = new Set(["mostly_no", "no"]);

// The four answers this card currently shows. Two rules are applied here:
// - sequential: once a criterion is No, every later one is blank;
// - path rule (§4): an asset on no modelled path has Interaction No once its
//   Feasibility is answered with anything but No.
function currentAnswers(candidate, edits) {
  const start = (key) => {
    if (key in edits) return edits[key] || null;
    if (candidate.human_confirmed) return candidate[`criterion_${key}`];
    if (candidate.blind_first) return null;
    return candidate[`ai_suggested_${key}`]; // route A: the AI's answer pre-fills the card
  };
  const out = {};
  let stopped = false;
  for (const [key] of CRITERIA) {
    out[key] = stopped ? null : start(key) ?? null;
    if (key === "attacker_reach" && candidate.n_paths === 0 && out.decoy_exists && out.decoy_exists !== "no")
      out[key] = "no";
    if (out[key] === "no") stopped = true;
  }
  return out;
}

// Criteria that come after a No, so cannot be answered (the first No ends the card).
function afterNo(answers) {
  const idx = CRITERIA.findIndex(([k]) => answers[k] === "no");
  return new Set(idx < 0 ? [] : CRITERIA.slice(idx + 1).map(([k]) => k));
}

function missing(answers) {
  for (const [key, name] of CRITERIA) {
    if (answers[key] === "no") return null;
    if (!answers[key]) return name;
  }
  return null;
}

function reasonTriggers(candidate, answers) {
  // Mirrors src/plausibility reason_required(); the API enforces it.
  const t = [];
  if (candidate.blind_first) t.push("blind card");
  else {
    const ai = CRITERIA.map(([k]) => candidate[`ai_suggested_${k}`] ?? null);
    if (ai.every((v) => v === null)) t.push("no AI suggestion — this is a direct score");
    else {
      const changed = CRITERIA.filter(([k], i) => (answers[k] ?? null) !== ai[i]).map(([, n]) => n);
      if (changed.length) t.push(`you changed the AI's answer on ${changed.join(", ")}`);
    }
  }
  const boundary = CRITERIA.filter(
    ([k]) => BOUNDARY.has(answers[k]) && !(k === "attacker_reach" && candidate.n_paths === 0)
  ).map(([, n]) => n);
  if (boundary.length) t.push(`Mostly No or No on ${boundary.join(", ")}`);
  if (candidate.n_paths > 1)
    t.push(`on ${candidate.n_paths} attack paths: give each path's Interaction level (weakest path decides)`);
  return t;
}

function PathSteps({ steps }) {
  if (!steps.length)
    return <p className="paths none">On no modelled attack path. Interaction is No by §4's rule.</p>;
  return (
    <ul className="paths">
      {steps.map((s, i) => (
        <li key={i}>
          <strong>{s.path}</strong> · step {s.step_order} of {s.path_length} · {s.tactic} ·{" "}
          {[s.technique_id, s.technique_name].filter(Boolean).join(" ")}
        </li>
      ))}
    </ul>
  );
}

function CandidateCard({ candidate, onSaved }) {
  const [edits, setEdits] = useState({});
  const [reason, setReason] = useState(candidate.human_reason ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const answers = currentAnswers(candidate, edits);
  const gap = missing(answers);
  const triggers = gap ? [] : reasonTriggers(candidate, answers);
  const needsReason = triggers.length > 0;
  const dirty = Object.keys(edits).length > 0 || reason !== (candidate.human_reason ?? "");
  const confirmed = !!candidate.human_confirmed;
  const canSubmit = !gap && (!needsReason || reason.trim()) && (!confirmed || dirty) && !saving;

  function choose(key, value) {
    setError(null);
    setEdits((prev) => {
      const next = { ...prev, [key]: value };
      // A No ends the card: clear every later criterion.
      if (value === "no") {
        const idx = CRITERIA.findIndex(([k]) => k === key);
        CRITERIA.slice(idx + 1).forEach(([k]) => (next[k] = ""));
      }
      return next;
    });
  }

  async function submit() {
    setSaving(true);
    setError(null);
    try {
      const body = Object.fromEntries(CRITERIA.map(([k]) => [k, answers[k]]));
      body.reason = reason.trim() || null;
      const res = await fetch(`${API}/candidates/${candidate.asset_id}/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail ?? `Server returned ${res.status}`);
      setEdits({});
      onSaved();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  let status;
  if (confirmed) status = candidate.passes_plausibility ? ["Confirmed — on the shortlist", "chip ok"] : ["Confirmed — excluded", "chip out"];
  else if (candidate.blind_first) status = ["Blind card — AI answer hidden until you confirm", "chip blind"];
  else if (candidate.ai_model) status = ["AI first pass — check each answer", "chip ai"];
  else status = ["No AI suggestion yet", "chip wait"];

  const locked = afterNo(answers);
  return (
    <div className={`card${candidate.blind_first ? " card-blind" : ""}`}>
      <div className="card-header">
        <div>
          <p className="asset-name">{candidate.name}</p>
          <p className="meta">
            {candidate.asset_type} · {candidate.zone} · Purdue level {candidate.purdue_level}
          </p>
        </div>
        <span className={status[1]}>{status[0]}</span>
      </div>

      <PathSteps steps={candidate.path_steps} />
      {candidate.n_paths > 1 && (
        <p className="hint">
          On {candidate.n_paths} paths: judge Interaction for each path, record the lowest, and give each path's
          level in your reason (weakest path decides, §4).
        </p>
      )}

      {!confirmed && !candidate.blind_first && !candidate.ai_model && (
        <p className="hint">
          Route A: wait for the notebook's suggestions. Scoring this card now is a direct (route B) score and needs a reason.
        </p>
      )}

      <div className="criteria">
        {CRITERIA.map(([key, name, question]) => {
          const disabled = locked.has(key) || (key === "attacker_reach" && candidate.n_paths === 0);
          return (
            <label key={key} className={`criterion${disabled ? " criterion-off" : ""}`} title={question}>
              <span className="criterion-name">{name}</span>
              <select
                className="badge-select"
                value={answers[key] ?? ""}
                disabled={disabled}
                onChange={(e) => choose(key, e.target.value)}
              >
                <option value="">—</option>
                {LEVELS.map(([v, l]) => (
                  <option key={v} value={v}>{l}</option>
                ))}
              </select>
            </label>
          );
        })}
      </div>

      {!candidate.ai_hidden && candidate.ai_reasoning && (
        <div className="ai-block">
          <p className="ai-label">
            AI{candidate.ai_model ? ` (${candidate.ai_model})` : ""}
            {candidate.blind_first
              ? " — shown after your blind confirmation. Your first answers below are kept as given; a later change alters only the final answers"
              : ""}
          </p>
          {!!candidate.blind_first && !!candidate.blind_confirmed_at && (
            <p className="agreement">
              {CRITERIA.map(([k, n]) => {
                const ai = candidate[`ai_suggested_${k}`];
                const you = candidate[`blind_${k}`]; // your first, blind answer, fixed when first confirmed
                if (!ai && !you) return null;
                return (
                  <span key={k} className={ai === you ? "agree" : "disagree"}>
                    {n}: you {LABEL[you] ?? "—"}, AI {LABEL[ai] ?? "—"}
                  </span>
                );
              })}
            </p>
          )}
          <p className="reasoning">{candidate.ai_reasoning}</p>
        </div>
      )}

      <label className="reason">
        <span>
          Your reason{needsReason ? " (required: " + triggers.join("; ") + ")" : " (optional)"}
        </span>
        <textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} />
      </label>

      <div className="card-footer">
        {gap && <span className="hint">Answer {gap} next.</span>}
        {error && <span className="error">{error}</span>}
        <button className={confirmed && !dirty ? "btn btn-confirmed" : "btn"} onClick={submit} disabled={!canSubmit}>
          {saving ? "Saving…" : confirmed ? (dirty ? "Save change" : "Confirmed") : "Confirm"}
        </button>
      </div>
    </div>
  );
}

export default function PlausibilityReview() {
  const [candidates, setCandidates] = useState(null);
  const [error, setError] = useState(null);

  function load() {
    fetch(`${API}/candidates`)
      .then((r) => {
        if (!r.ok) throw new Error(`Backend returned ${r.status}`);
        return r.json();
      })
      .then(setCandidates)
      .catch((e) => setError(e.message));
  }
  useEffect(load, []);

  if (error) {
    return (
      <div className="app">
        <p className="error">
          Can't reach the backend at {API} — is `uvicorn src.api.main:app` running? ({error})
        </p>
      </div>
    );
  }
  if (!candidates) return <div className="app"><p>Loading candidates…</p></div>;

  const blind = candidates.filter((c) => c.blind_first);
  const rest = candidates.filter((c) => !c.blind_first);
  const confirmedCount = candidates.filter((c) => c.human_confirmed).length;
  const shortlisted = candidates.filter((c) => c.human_confirmed && c.passes_plausibility).length;

  return (
    <div className="app">
      <h1>Plausibility review</h1>
      <p className="subtitle">
        {confirmedCount} of {candidates.length} confirmed · {shortlisted} on the shortlist ·{" "}
        {blind.filter((c) => c.human_confirmed).length} of {blind.length} blind cards done
      </p>
      <p className="rules">
        Answer the four criteria in order; the first No ends the card. Write a reason on blind cards, when you
        change an AI answer, and for any Mostly No or No. Level definitions: formal-problem-definition.md §4.
      </p>

      <h2>Blind cards — score these first</h2>
      {blind.map((c) => (
        <CandidateCard key={`${c.asset_id}-${c.confirmed_at ?? ""}-${c.ai_model ?? ""}`} candidate={c} onSaved={load} />
      ))}

      <h2>Review</h2>
      {rest.map((c) => (
        <CandidateCard key={`${c.asset_id}-${c.confirmed_at ?? ""}-${c.ai_model ?? ""}`} candidate={c} onSaved={load} />
      ))}
    </div>
  );
}
