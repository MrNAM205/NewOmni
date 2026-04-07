export function TriggerFeed({ triggers }) {
  return (
    &lt;div className="trigger-feed"&gt;
      {triggers.map((t, i) =&gt; (
        &lt;div key={i} className={`trigger ${t.type}`}&gt;
          {t.message}
        &lt;/div&gt;
      ))}
    &lt;/div&gt;
  );
}
