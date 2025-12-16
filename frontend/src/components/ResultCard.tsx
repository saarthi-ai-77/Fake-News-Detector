import { ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface ResultCardProps {
  title: string;
  icon: LucideIcon;
  children: ReactNode;
  delay?: number;
}

/**
 * Reusable result card component with consistent styling
 * Used for displaying analysis results in a card format
 */
const ResultCard = ({ title, icon: Icon, children, delay = 0 }: ResultCardProps) => {
  return (
    <Card 
      className="bg-card shadow-card border-border/40 card-hover animate-fade-in-up"
      style={{ animationDelay: `${delay}s` }}
    >
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg font-serif text-foreground">
          <Icon className="w-5 h-5 text-accent" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
    </Card>
  );
};

export default ResultCard;
