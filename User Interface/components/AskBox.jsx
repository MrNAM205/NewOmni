import { useState } from "react";

export default function AskBox({ onAsk }) {
  const [query, setQuery] = useState("");

  const submit = () => {
    if (!query.trim()) return;
    onAsk(query);
    setQuery("");
  };

  return (
    <div className="ask-box">
      <input
        type="text"
        placeholder="Ask about this mission…"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button onClick={submit}>Ask</button>
    </div>
  );
}
