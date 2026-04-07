export function CaseStatusBadge({ posture }) {
  return (
    &lt;span className={`case-status ${posture}`}&gt;
      {posture.toUpperCase()}
    &lt;/span&gt;
  );
}
