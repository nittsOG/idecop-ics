import { useState } from "react";
import Dashboard from "./Dashboard.jsx";
import PlausibilityReview from "./PlausibilityReview.jsx";
import SensitivitySweep from "./SensitivitySweep.jsx";

// The three screens of 02-prototype-architecture.md §3: the Dashboard (Screen 1),
// the sensitivity sweep (Screen 2, D46) and the Plausibility Review (Screen 3).
const SCREENS = {
  dashboard: { label: "Dashboard", element: <Dashboard /> },
  sweep: { label: "Sensitivity Sweep", element: <SensitivitySweep /> },
  review: { label: "Plausibility Review", element: <PlausibilityReview /> },
};

export default function App() {
  const [screen, setScreen] = useState("dashboard");
  return (
    <div>
      <nav style={{ display: "flex", gap: 8, padding: 12, borderBottom: "1px solid #eee", alignItems: "center" }}>
        <strong style={{ marginRight: 16 }}>iDECOP-ICS</strong>
        {Object.entries(SCREENS).map(([key, s]) => (
          <button key={key} onClick={() => setScreen(key)} aria-pressed={screen === key}>{s.label}</button>
        ))}
      </nav>
      {SCREENS[screen].element}
    </div>
  );
}
