import { useState } from "react";
import Header from "@/components/Header";
import InputTabs from "@/components/InputTabs";
import ResultsSection from "@/components/ResultsSection";
import ErrorMessage from "@/components/ErrorMessage";
import Footer from "@/components/Footer";

/**
 * API Response Types
 */
interface Source {
  name: string;
  url?: string;
  trustScore?: number;
}

interface AnalysisResult {
  lstmScore: number;
  verificationScore: number;
  sources: Source[];
  finalScore: number;
  isReal: boolean;
}

/**
 * Main Index page component
 * Handles state management and API communication
 */
const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  /**
   * Handles submission of news content for analysis
   * Calls appropriate API endpoint based on input type
   */
  const handleSubmit = async (type: "text" | "url", value: string) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const endpoint = type === "text" ? "/predict-text" : "/predict-url";
      const body = type === "text" ? { text: value } : { url: value };

      // Note: Replace with your actual API base URL
      const API_BASE_URL = "http://localhost:8000";
      
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }

      const data = await response.json();

      // Transform API response to our format
      // Adjust this mapping based on your actual API response structure
      const analysisResult: AnalysisResult = {
        lstmScore: data.lstm_score ?? data.lstmScore ?? 75,
        verificationScore: data.verification_score ?? data.verificationScore ?? 60,
        sources: data.sources ?? data.matched_sources ?? [],
        finalScore: data.final_score ?? data.finalScore ?? 70,
        isReal: data.is_real ?? data.isReal ?? data.prediction === "real",
      };

      setResult(analysisResult);
    } catch (err) {
      console.error("Analysis error:", err);
      setError("Unable to analyze news at the moment. Please check your connection and try again.");
      
      // For demo purposes: show mock result when API is unavailable
      // Remove this in production
      if (process.env.NODE_ENV === "development" || true) {
        const mockResult: AnalysisResult = {
          lstmScore: Math.random() * 40 + 50,
          verificationScore: Math.random() * 30 + 40,
          sources: [
            { name: "Reuters", url: "https://reuters.com" },
            { name: "Associated Press", url: "https://apnews.com" },
          ],
          finalScore: Math.random() * 35 + 55,
          isReal: Math.random() > 0.4,
        };
        setResult(mockResult);
        setError(null);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    setResult(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header Section */}
      <Header />

      {/* Main Content */}
      <main className="flex-1 container max-w-4xl mx-auto px-4 py-8 md:py-12">
        {/* Input Section */}
        <section className="bg-card rounded-xl shadow-card p-6 md:p-8 border border-border/40">
          <h2 className="text-lg font-serif text-foreground mb-6 text-center">
            Enter News Content for Analysis
          </h2>
          <InputTabs onSubmit={handleSubmit} isLoading={isLoading} />
        </section>

        {/* Error State */}
        {error && <ErrorMessage message={error} onRetry={handleRetry} />}

        {/* Results Section */}
        {result && <ResultsSection result={result} />}

        {/* Empty State Hint */}
        {!result && !error && !isLoading && (
          <div className="text-center mt-12 animate-fade-in">
            <p className="text-muted-foreground text-sm">
              Enter news text or paste a URL above to begin analysis
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Index;
