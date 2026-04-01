import { useEffect, useState } from "react";

export default function DocumentViewer({ documentId, onClose }) {
  const [doc, setDoc] = useState(null);

  useEffect(() => {
    if (!documentId) return;

    window.api.invoke("documents:get", { documentId })
      .then(setDoc);
  }, [documentId]);

  if (!documentId) return null;

  return (
    <div className="doc-modal">
      <div className="doc-backdrop" onClick={onClose} />

      <div className="doc-panel">
        <div className="doc-header">
          <h2>Document {documentId}</h2>
          <button onClick={onClose}>×</button>
        </div>

        {!doc && <p>Loading…</p>}

        {doc && (
          <>
            <div className="doc-meta">
              <p><strong>Path:</strong> {doc.metadata.path}</p>
              <p><strong>Source:</strong> {doc.metadata.source}</p>
              <p><strong>Created:</strong> {doc.metadata.created_at}</p>
            </div>

            <div className="doc-content">
              <pre>{doc.content}</pre>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
