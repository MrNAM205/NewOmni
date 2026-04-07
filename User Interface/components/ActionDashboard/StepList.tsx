export function StepList({ steps }) {
  return (
    &lt;div className="step-list"&gt;
      {Object.entries(steps).map(([step, status]) =&gt; (
        &lt;StepItem key={step} step={step} status={status} /&gt;
      ))}
    &lt;/div&gt;
  );
}
