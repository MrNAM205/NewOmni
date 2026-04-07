export function CaseRow({ caseData }) {
  return (
    &lt;div className="case-row"&gt;
      &lt;div className="case-title"&gt;{caseData.title}&lt;/div&gt;
      &lt;CaseStatusBadge posture={caseData.posture} /&gt;
      &lt;CaseProgressBar steps={caseData.steps} /&gt;
      &lt;CaseTriggers triggers={caseData.triggers} /&gt;
    &lt;/div&gt;
  );
}
