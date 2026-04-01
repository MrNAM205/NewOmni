export default function DocumentsTab({ documentGroups }) {
  return (
    <div>
      {Object.entries(documentGroups).map(([group, ids]) => (
        <div key={group}>
          <h4>{group}</h4>
          <ul>
            {ids.map(id => <li key={id}>Document {id}</li>)}
          </ul>
        </div>
      ))}
    </div>
  );
}
