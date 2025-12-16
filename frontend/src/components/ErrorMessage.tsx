import { AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

/**
 * Error message component for displaying API or validation errors
 * Includes optional retry functionality
 */
const ErrorMessage = ({ message, onRetry }: ErrorMessageProps) => {
  return (
    <Card className="border-destructive/30 bg-destructive/5 animate-fade-in mt-8">
      <CardContent className="flex flex-col items-center py-8">
        <AlertCircle className="w-12 h-12 text-destructive mb-4" />
        <p className="text-foreground font-medium text-center mb-2">
          Analysis Failed
        </p>
        <p className="text-sm text-muted-foreground text-center max-w-md">
          {message}
        </p>
        {onRetry && (
          <Button
            variant="outline"
            onClick={onRetry}
            className="mt-4 gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Try Again
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

export default ErrorMessage;
