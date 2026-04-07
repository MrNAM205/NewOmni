export function GlobalExecutionBoard({ cases }) {
  return (
    &lt;div className="global-execution-board"&gt;
      {cases.map((c) =&gt; (
        &lt;CaseRow key={c.id} caseData={c} /&gt;
      ))}
    &lt;/div&gt;
  );
}
