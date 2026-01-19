import { useState } from "react";
import CampaignForm from "./components/CampaignForm";
import CampaignResults from "./components/CampaignResults";
import type { CampaignBrief, CampaignResponse } from "./types/campaign";
import { generateFullCampaign } from "./services/api";
import "./App.css";

function App() {
  const [result, setResult] = useState<CampaignResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (brief: CampaignBrief) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await generateFullCampaign(brief);
      setResult(response);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Social Market</h1>
        <p>Create engaging social media content for your UK business in seconds</p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <p>{error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        {result ? (
          <CampaignResults result={result} onReset={handleReset} />
        ) : (
          <CampaignForm onSubmit={handleSubmit} isLoading={isLoading} />
        )}
      </main>

      <footer className="app-footer">
        <p>Made for UK small businesses</p>
      </footer>
    </div>
  );
}

export default App;
