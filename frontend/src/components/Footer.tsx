/**
 * Footer component with project attribution
 * Academic styling for university project demo
 */
const Footer = () => {
  return (
    <footer className="w-full py-6 mt-auto border-t border-border/50">
      <div className="container max-w-4xl mx-auto px-4">
        <p className="text-center text-sm text-muted-foreground">
          Fake News Detection System — University Research Project
        </p>
        <p className="text-center text-xs text-muted-foreground/70 mt-1">
          Powered by LSTM Deep Learning & Web Source Verification
        </p>
      </div>
    </footer>
  );
};

export default Footer;
