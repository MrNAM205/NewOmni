export function StepItem({ step, status }) {
  return (
    &lt;div className={`step-item status-${status}`}&gt;
      &lt;span&gt;{step}&lt;/span&gt;
      &lt;span className="status-badge"&gt;{status}&lt;/span&gt;
    &lt;/div&gt;
  );
}
