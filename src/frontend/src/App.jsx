import { useState } from "react";
import Dashboard from "./Dashboard.jsx";
import PlausibilityReview from "./PlausibilityReview.jsx";

// Two screens wired so far: Dashboard (Screen 1) and Plausibility Review
// (Screen 3, built earlier). Screen 2 (sensitivity-sweep comparison) isn't
// built yet — needs Phase D's actual sweep runs to be meaningful.
export default function App() {
  const [screen, setScreen] = useState("dashboard");
  return (
    <div>
      <nav style={{ display: "flex", gap: 8, padding: 12, borderBottom: "1px solid #eee", alignItems: "center" }}>
        <strong style={{ marginRight: 16 }}>iDECOP-ICS</strong>
        <button onClick={() => setScreen("dashboard")}>Dashboard</button>
        <button onClick={() => setScreen("review")}>Plausibility Review</button>
      </nav>
      {screen === "dashboard" ? <Dashboard /> : <PlausibilityReview />}
    </div>
  );
}
