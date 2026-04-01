export default function SummaryPanel({ summary }) {
  return (
    <div className="summary-panel">
      <h2>Summary</h2>
      <p>{summary.summary_text}</p>

      <h3>What we know</h3>
      <ul>
        {summary.known.map((k, i) => <li key={i}>{k}</li>)}
      </ul>

      <h3>What we don’t know yet</h3>
      <ul>
        {summary.unknown.map((u, i) => <li key={i}>{u}</li>)}
      </ul>
    </div>
  );
}
