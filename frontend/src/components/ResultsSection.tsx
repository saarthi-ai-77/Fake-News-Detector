import { Brain, Globe, Scale } from "lucide-react";
import ResultCard from "./ResultCard";
import ProgressBar from "./ProgressBar";
import SourceList from "./SourceList";
import VerdictBadge from "./VerdictBadge";

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

interface ResultsSectionProps {
  result: AnalysisResult;
}

/**
 * Main results section displaying all analysis cards
 * Shows LSTM output, source verification, and final verdict
 */
const ResultsSection = ({ result }: ResultsSectionProps) => {
  return (
    <div className="space-y-6 mt-8">
      <h2 className="text-xl font-serif text-foreground text-center animate-fade-in">
        Analysis Results
      </h2>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Card 1: LSTM Model Output */}
        <ResultCard title="LSTM Model Analysis" icon={Brain} delay={0.1}>
          <div className="space-y-4">
            <ProgressBar
              value={result.lstmScore}
              label="Real News Probability"
              variant={result.lstmScore >= 50 ? "success" : "destructive"}
            />
            <p className="text-xs text-muted-foreground mt-3">
              Deep learning model confidence based on linguistic patterns and content analysis.
            </p>
          </div>
        </ResultCard>

        {/* Card 2: Source Verification */}
        <ResultCard title="Source Verification" icon={Globe} delay={0.2}>
          <SourceList
            sources={result.sources}
            verificationScore={result.verificationScore}
          />
        </ResultCard>

        {/* Card 3: Final Verdict */}
        <ResultCard title="Final Verdict" icon={Scale} delay={0.3}>
          <VerdictBadge
            isReal={result.isReal}
            confidence={result.finalScore}
          />
        </ResultCard>
      </div>
    </div>
  );
};

export default ResultsSection;
