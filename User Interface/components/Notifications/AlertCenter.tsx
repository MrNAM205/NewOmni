export function AlertCenter({ alerts }) {
  return (
    <div className="alert-center">
      {alerts.map((a, i) => (
        <AlertItem key={i} alert={a} />
      ))}
    </div>
  );
}
