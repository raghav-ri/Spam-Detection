const Result = ({ result }) => {
  if (!result) return null;

  return (
    <div className="result">
      Result: <strong>{result}</strong>
    </div>
  );
};

export default Result;
