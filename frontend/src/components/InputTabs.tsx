import { useState } from "react";
import { FileText, Link, Search, Loader2 } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface InputTabsProps {
  onSubmit: (type: "text" | "url", value: string) => void;
  isLoading: boolean;
}

/**
 * Tabbed input component for text or URL submission
 * Handles validation and provides visual feedback
 */
const InputTabs = ({ onSubmit, isLoading }: InputTabsProps) => {
  const [activeTab, setActiveTab] = useState<"text" | "url">("text");
  const [textInput, setTextInput] = useState("");
  const [urlInput, setUrlInput] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    setError("");
    
    if (activeTab === "text") {
      if (!textInput.trim()) {
        setError("Please enter some news text to analyze.");
        return;
      }
      if (textInput.trim().length < 50) {
        setError("Please enter at least 50 characters for accurate analysis.");
        return;
      }
      onSubmit("text", textInput.trim());
    } else {
      if (!urlInput.trim()) {
        setError("Please enter a URL to analyze.");
        return;
      }
      // Basic URL validation
      try {
        new URL(urlInput.trim());
        onSubmit("url", urlInput.trim());
      } catch {
        setError("Please enter a valid URL (e.g., https://example.com/article).");
      }
    }
  };

  return (
    <div className="w-full animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as "text" | "url")} className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-6 bg-secondary/50">
          <TabsTrigger 
            value="text" 
            className="flex items-center gap-2 data-[state=active]:bg-card data-[state=active]:shadow-soft"
          >
            <FileText className="w-4 h-4" />
            Text Input
          </TabsTrigger>
          <TabsTrigger 
            value="url" 
            className="flex items-center gap-2 data-[state=active]:bg-card data-[state=active]:shadow-soft"
          >
            <Link className="w-4 h-4" />
            URL Input
          </TabsTrigger>
        </TabsList>

        <TabsContent value="text" className="mt-0">
          <div className="space-y-4">
            <Textarea
              placeholder="Paste news article text here for analysis...

Example: Enter the full text of a news article you want to verify. The LSTM model will analyze the content patterns and linguistic features to determine authenticity."
              value={textInput}
              onChange={(e) => {
                setTextInput(e.target.value);
                setError("");
              }}
              className="min-h-[200px] resize-none bg-card border-border/60 focus:border-primary/50 transition-colors"
              disabled={isLoading}
            />
            <p className="text-xs text-muted-foreground">
              {textInput.length} characters entered (minimum 50 recommended)
            </p>
          </div>
        </TabsContent>

        <TabsContent value="url" className="mt-0">
          <div className="space-y-4">
            <Input
              type="url"
              placeholder="https://example.com/news-article"
              value={urlInput}
              onChange={(e) => {
                setUrlInput(e.target.value);
                setError("");
              }}
              className="h-12 bg-card border-border/60 focus:border-primary/50 transition-colors"
              disabled={isLoading}
            />
            <p className="text-xs text-muted-foreground">
              Enter the full URL of the news article you want to verify
            </p>
          </div>
        </TabsContent>
      </Tabs>

      {/* Error Message */}
      {error && (
        <p className="text-destructive text-sm mt-4 animate-fade-in">
          {error}
        </p>
      )}

      {/* Submit Button */}
      <Button
        onClick={handleSubmit}
        disabled={isLoading}
        className="w-full mt-6 h-12 text-base font-medium bg-primary hover:bg-primary/90 transition-all"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 mr-2 animate-spin-slow" />
            Analyzing news using LSTM model...
          </>
        ) : (
          <>
            <Search className="w-5 h-5 mr-2" />
            Verify News
          </>
        )}
      </Button>
    </div>
  );
};

export default InputTabs;
