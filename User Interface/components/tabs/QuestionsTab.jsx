export default function QuestionsTab({ questions }) {
  return (
    <div>
      <h4>For Nonprofits</h4>
      <ul>{questions.for_nonprofits.map((q, i) => <li key={i}>{q}</li>)}</ul>

      <h4>For Lawyers</h4>
      <ul>{questions.for_lawyers.map((q, i) => <li key={i}>{q}</li>)}</ul>

      <h4>For County</h4>
      <ul>{questions.for_county.map((q, i) => <li key={i}>{q}</li>)}</ul>
    </div>
  );
}
