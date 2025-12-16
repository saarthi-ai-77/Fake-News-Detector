import { Shield } from "lucide-react";

/**
 * Header component displaying the application title and subtitle
 * Uses academic styling with serif font for headings
 */
const Header = () => {
  return (
    <header className="w-full py-8 md:py-12 bg-primary text-primary-foreground">
      <div className="container max-w-4xl mx-auto px-4">
        <div className="flex items-center justify-center gap-3 mb-4">
          <Shield className="w-8 h-8 md:w-10 md:h-10" />
          <h1 className="text-2xl md:text-4xl font-serif tracking-tight">
            Fake News Detection System
          </h1>
        </div>
        <p className="text-center text-primary-foreground/80 text-sm md:text-base font-light">
          Hybrid Deep Learning (LSTM) and Web Source Verification Approach
        </p>
      </div>
    </header>
  );
};

export default Header;
