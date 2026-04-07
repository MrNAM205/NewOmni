export function CaseTriggers({ triggers }) {
  return (
    &lt;div className="case-triggers"&gt;
      {triggers.map((t, i) =&gt; (
        &lt;span key={i} className={`trigger ${t.type}`}&gt;
          {t.message}
        &lt;/span&gt;
      ))}
    &lt;/div&gt;
  );
}
