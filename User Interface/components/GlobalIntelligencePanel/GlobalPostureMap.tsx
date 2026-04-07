export function GlobalPostureMap({ posture }) {
  return (
    &lt;div className="global-posture-map"&gt;
      {Object.entries(posture).map(([key, count]) =&gt; (
        &lt;div key={key} className="posture-item"&gt;
          &lt;span className="label"&gt;{key}&lt;/span&gt;
          &lt;span className="count"&gt;{count}&lt;/span&gt;
        &lt;/div&gt;
      ))}
    &lt;/div&gt;
  );
}
