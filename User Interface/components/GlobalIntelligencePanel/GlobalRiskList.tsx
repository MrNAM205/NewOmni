export function GlobalRiskList({ risks }) {
  return (
    &lt;div className="global-risk-list"&gt;
      {risks.map((r, i) =&gt; (
        &lt;div key={i} className="risk-item"&gt;
          &lt;span className="case-id"&gt;Case {r.case_id}&lt;/span&gt;
          &lt;span className="issue"&gt;{r.issue.message}&lt;/span&gt;
        &lt;/div&gt;
      ))}
    &lt;/div&gt;
  );
}
