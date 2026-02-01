import { useState } from "react";

const SpamForm = ({ setResult }) => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("https://spam-detection-jl95.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setResult(data.prediction);
    } catch (err) {
      setResult("Server error");
    }

    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        placeholder="Enter SMS text here..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        required
      />

      <button type="submit">
        {loading ? "Checking..." : "Check Message"}
      </button>
    </form>
  );
};

export default SpamForm;
