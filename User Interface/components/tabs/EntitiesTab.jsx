export default function EntitiesTab({ entities }) {
  return (
    <div>
      {entities.map(e => (
        <div key={e.id}>
          {e.entity} ({e.entity_type})
        </div>
      ))}
    </div>
  );
}
