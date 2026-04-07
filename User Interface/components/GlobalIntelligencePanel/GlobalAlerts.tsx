export function GlobalAlerts({ alerts }) {
  return (
    &lt;div className="global-alerts"&gt;
      {alerts.map((a, i) =&gt; (
        &lt;div key={i} className={`alert ${a.type}`}&gt;
          {a.message}
        &lt;/div&gt;
      ))}
    &lt;/div&gt;
  );
}
