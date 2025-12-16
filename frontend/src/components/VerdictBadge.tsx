import { CheckCircle2, XCircle, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface VerdictBadgeProps {
  isReal: boolean;
  confidence: number;
}

/**
 * Badge component displaying the final verdict with appropriate styling
 * Shows green for real news, red for fake news
 */
const VerdictBadge = ({ isReal, confidence }: VerdictBadgeProps) => {
  const isHighConfidence = confidence >= 70;
  
  if (isReal) {
    return (
      <div className="flex flex-col items-center gap-3 py-4">
        <div className={`p-4 rounded-full ${isHighConfidence ? "bg-success/10" : "bg-success/5"}`}>
          <CheckCircle2 className={`w-12 h-12 ${isHighConfidence ? "text-success" : "text-success/70"}`} />
        </div>
        <Badge 
          className="px-4 py-2 text-base font-medium bg-success text-success-foreground border-0"
        >
          Likely Real News
        </Badge>
        <p className="text-sm text-muted-foreground">
          Combined confidence: {confidence.toFixed(1)}%
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-3 py-4">
      <div className={`p-4 rounded-full ${isHighConfidence ? "bg-destructive/10" : "bg-destructive/5"}`}>
        {isHighConfidence ? (
          <XCircle className="w-12 h-12 text-destructive" />
        ) : (
          <AlertCircle className="w-12 h-12 text-destructive/70" />
        )}
      </div>
      <Badge 
        className="px-4 py-2 text-base font-medium bg-destructive text-destructive-foreground border-0"
      >
        Likely Fake News
      </Badge>
      <p className="text-sm text-muted-foreground">
        Combined confidence: {confidence.toFixed(1)}%
      </p>
    </div>
  );
};

export default VerdictBadge;
