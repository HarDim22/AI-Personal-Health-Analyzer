import { useEffect, useState } from "react";
import "./App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  
function App() {
  const [form, setForm] = useState({
    glucose: "",
    hba1c: "",
    ldl: "",
    hdl: "",
    triglycerides: "",
    total_cholesterol: "",
    label: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [history, setHistory] = useState([]);
  const [historyError, setHistoryError] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(false);

  // AI-like summary state
  const [aiSummary, setAiSummary] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  // ===== CSS helpers ======

  const getStatusClass = (status) => {
    switch (status) {
      case "normal":
      case "good":
      case "optimal":
      case "desirable":
        return "status-badge status-normal";
      case "elevated":
      case "borderline_high":
      case "near_optimal":
        return "status-badge status-elevated";
      case "high":
      case "very_high":
      case "low":
        return "status-badge status-high";
      default:
        return "status-badge";
    }
  };

  const getOverallRiskClass = (risk) => {
    switch (risk) {
      case "high_risk":
        return "overall-risk overall-risk-high_risk";
      case "moderate_risk":
        return "overall-risk overall-risk-moderate_risk";
      default:
        return "overall-risk overall-risk-unknown";
    }
  };

  // ===== Helpers ======

  // For save-result (includes label)
  const buildSavePayload = () => {
    const payload = {};
    for (const [key, value] of Object.entries(form)) {
      if (key === "label") {
        if (value.trim() !== "") payload[key] = value.trim();
      } else if (value !== "") {
        payload[key] = Number(value);
      }
    }
    return payload;
  };

  // For ai-summary (only lab values)
  const buildLabsPayload = () => {
    const { label, ...rest } = form;
    const payload = {};
    for (const [key, value] of Object.entries(rest)) {
      if (value !== "") {
        payload[key] = Number(value);
      }
    }
    return payload;
  };

  const fetchHistory = async () => {
    setLoadingHistory(true);
    setHistoryError("");
    try {
      const res = await fetch(`${API_BASE_URL}/history`);
      if (!res.ok) throw new Error("Error fetching history");
      const data = await res.json();
      setHistory(data);
    } catch (err) {
      console.error(err);
      setHistoryError("Could not load history.");
    } finally {
      setLoadingHistory(false);
    }
  };

  // ===== Handlers ======

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    setAiSummary(null); // reset AI summary when new analysis is run
    setAiError("");

    const payload = buildSavePayload();

    try {
      const response = await fetch(`${API_BASE_URL}/save-result`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const text = await response.text();
        console.error("API error:", response.status, text);
        throw new Error("API error");
      }

      const entry = await response.json();
      setResult(entry.analysis);
      await fetchHistory();
    } catch (err) {
      console.error(err);
      setError("Could not connect to backend API.");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAiSummary = async () => {
    setAiLoading(true);
    setAiError("");
    setAiSummary(null);

    const labsPayload = buildLabsPayload();

    if (Object.keys(labsPayload).length === 0) {
      setAiLoading(false);
      setAiError("Please enter at least one lab value before requesting an explanation.");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/ai-summary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(labsPayload),
      });

      if (!response.ok) {
        const text = await response.text();
        console.error("AI summary API error:", response.status, text);
        throw new Error("AI summary API error");
      }

      const data = await response.json();
      setAiSummary(data.ai_summary);
    } catch (err) {
      console.error(err);
      setAiError("Could not generate explanation.");
    } finally {
      setAiLoading(false);
    }
  };

  // Load history on first render
  useEffect(() => {
    fetchHistory();
  }, []);

  // Build chart data for glucose
  const glucoseData = history
    .filter((entry) => entry.input && entry.input.glucose !== undefined)
    .map((entry) => ({
      date: entry.created_at ? entry.created_at.slice(0, 10) : "",
      glucose: entry.input.glucose,
      label: entry.label || "",
    }))
    .reverse();

  return (
    <div className="container">
      <h1>AI Personal Health Analyzer</h1>
      <p>
        Enter your lab values (leave empty if you don't have a specific test).
        Each analysis is also saved to your history.
      </p>

      {/* FORM */}
      <form onSubmit={handleSubmit} className="form-grid">
        <input
          type="text"
          name="label"
          placeholder="Label (e.g. 'Check-up January')"
          value={form.label}
          onChange={handleChange}
        />

        <input
          type="number"
          name="glucose"
          placeholder="Fasting Glucose (mg/dL)"
          value={form.glucose}
          onChange={handleChange}
          step="0.1"
        />

        <input
          type="number"
          name="hba1c"
          placeholder="HbA1c (%)"
          value={form.hba1c}
          onChange={handleChange}
          step="0.1"
        />

        <input
          type="number"
          name="ldl"
          placeholder="LDL (mg/dL)"
          value={form.ldl}
          onChange={handleChange}
          step="0.1"
        />

        <input
          type="number"
          name="hdl"
          placeholder="HDL (mg/dL)"
          value={form.hdl}
          onChange={handleChange}
          step="0.1"
        />

        <input
          type="number"
          name="triglycerides"
          placeholder="Triglycerides (mg/dL)"
          value={form.triglycerides}
          onChange={handleChange}
          step="0.1"
        />

        <input
          type="number"
          name="total_cholesterol"
          placeholder="Total Cholesterol (mg/dL)"
          value={form.total_cholesterol}
          onChange={handleChange}
          step="0.1"
        />

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing & saving..." : "Analyze & Save"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* RESULTS */}
      {result && (
        <div className="result-box">
          <h2>
            Overall Risk:{" "}
            <span className={getOverallRiskClass(result.overall_risk)}>
              {result.overall_risk}
            </span>
          </h2>

          {result.summary && (
            <p style={{ marginTop: "8px", marginBottom: "16px" }}>
              <strong>Summary:</strong> {result.summary}
            </p>
          )}

          <ul>
            {result.items.map((item, index) => (
              <li key={index} className="result-item">
                <strong>{item.name}</strong> — {item.value} {item.unit}
                <br />
                <span className={getStatusClass(item.status)}>
                  Status: {item.status}
                </span>
                <br />
                <small>Reference: {item.reference_range}</small>
                <br />
                {item.message}
              </li>
            ))}
          </ul>

          {/* AI-like explanation section */}
          <div style={{ marginTop: "16px" }}>
            <button
              type="button"
              onClick={handleGenerateAiSummary}
              disabled={aiLoading}
            >
              {aiLoading
                ? "Generating AI-style explanation..."
                : "Generate AI-style Explanation"}
            </button>

            {aiError && <p style={{ color: "red", marginTop: "8px" }}>{aiError}</p>}

            {aiSummary && (
              <div
                style={{
                  marginTop: "12px",
                  padding: "12px",
                  borderRadius: "8px",
                  background: "#f7fafc",
                  border: "1px solid #e2e8f0",
                }}
              >
                <h3>AI-style Explanation</h3>
                <p style={{ marginTop: "6px" }}>{aiSummary.general_overview}</p>

                {aiSummary.detailed_points && aiSummary.detailed_points.length > 0 && (
                  <>
                    <h4 style={{ marginTop: "10px" }}>Key points:</h4>
                    <ul>
                      {aiSummary.detailed_points.map((p, i) => (
                        <li key={i}>{p}</li>
                      ))}
                    </ul>
                  </>
                )}

                {aiSummary.lifestyle_tips && aiSummary.lifestyle_tips.length > 0 && (
                  <>
                    <h4 style={{ marginTop: "10px" }}>General lifestyle ideas:</h4>
                    <ul>
                      {aiSummary.lifestyle_tips.map((p, i) => (
                        <li key={i}>{p}</li>
                      ))}
                    </ul>
                  </>
                )}

                <p style={{ marginTop: "10px", fontSize: "12px", color: "#4a5568" }}>
                  {aiSummary.disclaimer}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* HISTORY & CHART SECTION */}
      <div className="history-section">
        <h2>History & Trends</h2>

        {loadingHistory && <p>Loading history...</p>}
        {historyError && <p style={{ color: "red" }}>{historyError}</p>}

        {/* Chart */}
        {glucoseData.length > 0 && (
          <div className="chart-card">
            <h3>Fasting Glucose Over Time</h3>
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={glucoseData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="glucose" stroke="#3182ce" dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Simple history list */}
        {history.length > 0 && (
          <div className="history-list">
            <h3>Recent Analyses</h3>
            <ul>
              {history.map((entry) => (
                <li key={entry.id} className="history-item">
                  <strong>{entry.label || "Unnamed check"}</strong> —{" "}
                  {entry.created_at
                    ? entry.created_at.replace("T", " ").slice(0, 16)
                    : ""}
                  <br />
                  <small>
                    Glucose:{" "}
                    {entry.input.glucose !== undefined
                      ? `${entry.input.glucose} mg/dL`
                      : "N/A"}
                    , HbA1c:{" "}
                    {entry.input.hba1c !== undefined
                      ? `${entry.input.hba1c}%`
                      : "N/A"}
                  </small>
                </li>
              ))}
            </ul>
          </div>
        )}

        {history.length === 0 && !loadingHistory && (
          <p>No analyses saved yet. Run an analysis to start your history.</p>
        )}
      </div>
    </div>
  );
}

export default App;
