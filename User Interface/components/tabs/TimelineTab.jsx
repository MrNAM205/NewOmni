export default function TimelineTab({ timeline }) {
  return (
    <div>
      {timeline.map(ev => (
        <div key={ev.id}>
          <strong>{ev.event_date || "No date"}</strong>: {ev.event_text}
        </div>
      ))}
    </div>
  );
}
