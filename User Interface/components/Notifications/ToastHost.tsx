export function ToastHost({ toasts }) {
  return (
    <div className="toast-host">
      {toasts.map((t) => (
        <Toast key={t.id} alert={t} />
      ))}
    </div>
  );
}
