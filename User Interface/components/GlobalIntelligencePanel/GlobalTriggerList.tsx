export function GlobalTriggerList({ triggers }) {
  return (
    &lt;div className="global-trigger-list"&gt;
      {triggers.map((t, i) =&gt; (
        &lt;div key={i} className={`trigger ${t.trigger.type}`}&gt;
          &lt;span className="case-id"&gt;Case {t.case_id}&lt;/span&gt;
          &lt;span className="message"&gt;{t.trigger.message}&lt;/span&gt;
        &lt;/div&gt;
      ))}
    &lt;/div&gt;
  );
}
