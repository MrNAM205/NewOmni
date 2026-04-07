export function CaseProgressBar({ steps }) {
  const total = Object.keys(steps).length;
  const completed = Object.values(steps).filter(s =&gt; s === "completed").length;

  const pct = Math.round((completed / total) * 100);

  return (
    &lt;div className="case-progress-bar"&gt;
      &lt;div className="fill" style={{ width: `${pct}%` }} /&gt;
    &lt;/div&gt;
  );
}
