export function Toast({ alert }) {
  return (
    <div className={`toast ${alert.priority}`}>
      <div className="toast-message">{alert.message}</div>
    </div>
  );
}
