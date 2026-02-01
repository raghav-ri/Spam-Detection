import { useState } from "react";

const SpamChecker = () => {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const checkSpam = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResult("");

    try {
      const response = await fetch(
        "https://spam-detection-jl95.onrender.com/predict",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message }),
        }
      );

      const data = await response.json();
      setResult(data.prediction);
    } catch (err) {
      setResult("Server error. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <div className="brand">
        <div className="logo">R</div>
        <span>Rsecure</span>
      </div>

      <h1>Check for scam text messages</h1>
      <p className="subtitle">
        AI-powered SMS scam detection using Machine Learning
      </p>

      <textarea
        placeholder="Paste the message here..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button onClick={checkSpam} disabled={loading}>
        {loading ? "Checking..." : "Check Message"}
      </button>

      {result && (
        <div
          className={`result ${
            result === "Spam" ? "spam" : "ham"
          }`}
        >
          Result: <strong>{result}</strong>
        </div>
      )}
    </div>
  );
};

export default SpamChecker;
