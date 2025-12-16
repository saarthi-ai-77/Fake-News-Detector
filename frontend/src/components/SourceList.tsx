import { ExternalLink, CheckCircle, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface Source {
  name: string;
  url?: string;
  trustScore?: number;
}

interface SourceListProps {
  sources: Source[];
  verificationScore: number;
}

/**
 * Component displaying matched trusted sources and verification status
 * Shows a list of sources with their trust scores
 */
const SourceList = ({ sources, verificationScore }: SourceListProps) => {
  const hasTrustedSources = sources.length > 0;

  return (
    <div className="space-y-4">
      {/* Verification Score */}
      <div className="flex items-center justify-between pb-3 border-b border-border/50">
        <span className="text-sm text-muted-foreground">Verification Score</span>
        <span className="text-lg font-semibold text-foreground">
          {verificationScore.toFixed(1)}%
        </span>
      </div>

      {/* Trust Badge */}
      <div className="flex justify-center py-2">
        {hasTrustedSources ? (
          <Badge className="flex items-center gap-2 px-3 py-1.5 bg-success/10 text-success border border-success/20">
            <CheckCircle className="w-4 h-4" />
            Trusted Sources Found
          </Badge>
        ) : (
          <Badge className="flex items-center gap-2 px-3 py-1.5 bg-destructive/10 text-destructive border border-destructive/20">
            <AlertTriangle className="w-4 h-4" />
            No Trusted Sources Found
          </Badge>
        )}
      </div>

      {/* Source List */}
      {hasTrustedSources && (
        <div className="space-y-2 pt-2">
          <p className="text-xs text-muted-foreground uppercase tracking-wide">
            Matched Sources
          </p>
          <ul className="space-y-2">
            {sources.map((source, index) => (
              <li 
                key={index}
                className="flex items-center justify-between p-2 rounded-md bg-secondary/30 animate-slide-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span className="text-sm font-medium">{source.name}</span>
                </div>
                {source.url && (
                  <a 
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-accent hover:text-accent/80 transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {!hasTrustedSources && (
        <p className="text-sm text-muted-foreground text-center py-2">
          No matching trusted sources were found for this content.
        </p>
      )}
    </div>
  );
};

export default SourceList;
