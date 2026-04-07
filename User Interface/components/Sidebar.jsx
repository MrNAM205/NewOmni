export default function Sidebar({
  missions,
  activeMissionId,
  onSelectMission,
  activePersona,
  onSelectPersona,
  onSelectPanel
}) {
  return (
    &lt;div className="sidebar"&gt;
      &lt;h3&gt;Dashboards&lt;/h3&gt;
      &lt;ul&gt;
        &lt;li onClick={() =&gt; onSelectPanel("global_intel")}&gt;
          Global Intelligence
        &lt;/li&gt;
      &lt;/ul&gt;

      &lt;h3&gt;Missions&lt;/h3&gt;
      &lt;ul&gt;
        {missions.map(m =&gt; (
          &lt;li
            key={m.id}
            className={m.id === activeMissionId ? "active" : ""}
            onClick={() =&gt; onSelectMission(m.id)}
          &gt;
            {m.name} — {m.description}
          &lt;/li&gt;
        ))}
      &lt;/ul&gt;

      &lt;h3&gt;Persona&lt;/h3&gt;
      &lt;select
        value={activePersona}
        onChange={e =&gt; onSelectPersona(e.target.value)}
      &gt;
        &lt;option value="private_individual"&gt;Private Individual&lt;/option&gt;
        &lt;option value="analyst"&gt;Analyst&lt;/option&gt;
        &lt;option value="representative"&gt;Representative&lt;/option&gt;
      &lt;/select&gt;
    &lt;/div&gt;
  );
}
