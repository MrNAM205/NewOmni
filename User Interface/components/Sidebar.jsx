export default function Sidebar({
  missions,
  activeMissionId,
  onSelectMission,
  activePersona,
  onSelectPersona
}) {
  return (
    <div className="sidebar">
      <h3>Missions</h3>
      <ul>
        {missions.map(m => (
          <li
            key={m.id}
            className={m.id === activeMissionId ? "active" : ""}
            onClick={() => onSelectMission(m.id)}
          >
            {m.name} — {m.description}
          </li>
        ))}
      </ul>

      <h3>Persona</h3>
      <select
        value={activePersona}
        onChange={e => onSelectPersona(e.target.value)}
      >
        <option value="private_individual">Private Individual</option>
        <option value="analyst">Analyst</option>
        <option value="representative">Representative</option>
      </select>
    </div>
  );
}
