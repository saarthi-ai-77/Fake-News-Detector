interface ProgressBarProps {
  value: number;
  label: string;
  variant?: "default" | "success" | "destructive";
}

/**
 * Animated progress bar component for displaying probability scores
 * Supports different color variants based on the result type
 */
const ProgressBar = ({ value, label, variant = "default" }: ProgressBarProps) => {
  const clampedValue = Math.max(0, Math.min(100, value));
  
  const getBarColor = () => {
    switch (variant) {
      case "success":
        return "bg-success";
      case "destructive":
        return "bg-destructive";
      default:
        return "bg-accent";
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center text-sm">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-semibold text-foreground">{clampedValue.toFixed(1)}%</span>
      </div>
      <div className="h-3 bg-secondary rounded-full overflow-hidden">
        <div
          className={`h-full ${getBarColor()} rounded-full transition-all duration-1000 ease-out`}
          style={{ width: `${clampedValue}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
