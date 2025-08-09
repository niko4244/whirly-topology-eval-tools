import React, { useEffect, useState } from "react";
import { startTraining, fetchTrainingStatus } from "../api/training";

export default function TrainingTrigger() {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function beginTraining(name) {
    setLoading(true);
    try {
      await startTraining(name);
      pollStatus();
    } catch (err) {
      setError("Training failed");
      setLoading(false);
    }
  }

  async function pollStatus() {
    let done = false;
    while (!done) {
      try {
        const res = await fetchTrainingStatus();
        setModules(res.data);
        done = res.data.every(tr => tr.status === "completed");
        await new Promise(r => setTimeout(r, 2000)); // Poll every 2s
      } catch {
        setError("Status polling failed");
        break;
      }
    }
    setLoading(false);
  }

  useEffect(() => { pollStatus(); }, []);

  return (
    <div>
      <button onClick={() => beginTraining("Main Training")} disabled={loading}>
        {loading ? "Training in progress..." : "Start Training"}
      </button>
      {error && <div>{error}</div>}
      <ul>
        {modules.map(m => (
          <li key={m.id}>
            {m.name}: {m.progress}% {m.status}
          </li>
        ))}
      </ul>
    </div>
  );
}