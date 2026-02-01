import { useState } from "react";
import Header from "./components/Header";
import SpamForm from "./components/SpamForm";
import Result from "./components/Result";
import "./App.css";

function App() {
  const [result, setResult] = useState("");

  return (
    <div className="app">
      <Header />
      <SpamForm setResult={setResult} />
      <Result result={result} />
    </div>
  );
}

export default App;
