export function PostureIndicator({ posture }) {
  return (
    &lt;div className={`posture-indicator ${posture}`}&gt;
      {posture.toUpperCase()}
    &lt;/div&gt;
  );
}
