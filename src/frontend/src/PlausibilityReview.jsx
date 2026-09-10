import { useEffect, useState } from "react";
import "./App.css";

// Screen 3 — plausibility review, built earlier. Unchanged logic, moved
// into its own file now that App.jsx hosts navigation between screens.
const API = "http://127.0.0.1:8000";

const CRITERIA = [
  ["decoy_exists", "criterion_decoy_exists", "ai_suggested_decoy_exists", "Can exist"],
  ["attacker_reach", "criterion_attacker_reach", "ai_suggested_attacker_reach", "Reachable"],
  ["useful_signal", "criterion_useful_signal", "ai_suggested_useful_signal", "Signal"],
  ["reliable_indicator", "criterion_reliable_indicator", "ai_suggested_reliable_indicator", "Reliable"],
];

function CandidateCard({ candidate, onConfirm }) {
  const [edits, setEdits] = useState({});
  const [saving, setSaving] = useState(false);

  const effective = (key, confirmedKey, aiKey) =>
    edits[key] ?? candidate[confirmedKey] ?? candidate[aiKey];

  const isConfirmed = !!candidate.confirmed_at && Object.keys(edits).length === 0;
  const wasEdited = Object.keys(edits).length > 0;

  async function submit() {
    setSaving(true);
    try {
      const body = Object.fromEntries(
        CRITERIA.map(([key]) => [
          key,
          edits[key] ?? candidate[`ai_suggested_${key}`] ?? candidate[`criterion_${key}`],
        ])
      );
      const res = await fetch(`${API}/candidates/${candidate.asset_id}/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const updated = await res.json();
      onConfirm(updated);
      setEdits({});
    } catch (err) {
      alert(`Confirm failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <p className="asset-name">{candidate.name}</p>
        <button
          className={isConfirmed ? "btn btn-confirmed" : wasEdited ? "btn btn-edited" : "btn"}
          onClick={submit}
          disabled={saving}
        >
          {saving ? "Saving…" : isConfirmed ? "Confirmed" : wasEdited ? "Save edit" : "Confirm"}
        </button>
      </div>
      <div className="badge-row">
        {CRITERIA.map(([key, confirmedKey, aiKey, label]) => (
          <select
            key={key}
            className="badge-select"
            value={effective(key, confirmedKey, aiKey) ?? ""}
            onChange={(e) => setEdits((prev) => ({ ...prev, [key]: e.target.value }))}
          >
            <option value="">{label}: —</option>
            <option value="yes">{label}: yes</option>
            <option value="mostly">{label}: mostly</option>
            <option value="no">{label}: no</option>
          </select>
        ))}
      </div>
      {candidate.ai_reasoning && <p className="reasoning">{candidate.ai_reasoning}</p>}
      {!candidate.ai_reasoning && candidate.rationale && (
        <p className="reasoning">{candidate.rationale}</p>
      )}
    </div>
  );
}

export default function PlausibilityReview() {
  const [candidates, setCandidates] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/candidates`)
      .then((r) => {
        if (!r.ok) throw new Error(`Backend returned ${r.status}`);
        return r.json();
      })
      .then(setCandidates)
      .catch((e) => setError(e.message));
  }, []);

  function handleConfirm(updated) {
    setCandidates((prev) =>
      prev.map((c) => (c.asset_id === updated.asset_id ? { ...c, ...updated } : c))
    );
  }

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

  return (
    <div className="app">
      <h1>Plausibility review</h1>
      <p className="subtitle">
        {candidates.filter((c) => c.confirmed_at).length} of {candidates.length} confirmed
      </p>
      {candidates.map((c) => (
        <CandidateCard key={c.asset_id} candidate={c} onConfirm={handleConfirm} />
      ))}
    </div>
  );
}
