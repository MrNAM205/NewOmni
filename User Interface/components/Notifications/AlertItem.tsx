export function AlertItem({ alert }) {
  return (
    <div className={`alert-item ${alert.priority}`}>
      <div className="alert-type">{alert.type}</div>
      <div className="alert-message">{alert.message}</div>
      {alert.case_id && (
        <div className="alert-case">Case {alert.case_id}</div>
      )}
    </div>
  );
}
