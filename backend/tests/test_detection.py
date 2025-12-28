
import unittest
from unittest.mock import patch
import sys
import os

# Ensure backend can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.main import calculate_verdict
    from backend.verify import analyze_snippet
except ImportError:
    from main import calculate_verdict
    from verify import analyze_snippet

class TestDetectionQuality(unittest.TestCase):

    def test_analyze_snippet_debunk(self):
        """Test if snippet analysis correctly identifies debunks."""
        title = "Fact Check: Did the moon land on Earth?"
        snippet = "Social media posts claim the moon crashed into Earth. We found this to be FALSE. It was a CGI hoax."
        score = analyze_snippet(title, snippet)
        self.assertLess(score, 0.6, "Should identify the debunk with a low score")

    def test_analyze_snippet_confirm(self):
        """Test if snippet analysis identifies positive reports."""
        title = "NASA's Webb Telescope Captures Pillars of Creation"
        snippet = "NASA released new high-resolution images of the Eagle Nebula, showing stars forming in the pillars."
        score = analyze_snippet(title, snippet)
        self.assertGreater(score, 1.0, "Should identify confirmation with a high score")

    def test_verdict_logic_debunk_dominance(self):
        """Test if low verification score pulls down even an uncertain LSTM score."""
        lstm_score = 0.52 # Uncertain
        verification_score = 0.2 # Strong debunk/no sources
        final_score, verdict, is_real = calculate_verdict(lstm_score, verification_score)
        
        self.assertFalse(is_real)
        self.assertEqual(verdict, "Likely Fake News")
        self.assertLess(final_score, 0.4)

    def test_verdict_logic_real_confirmation(self):
        """Test if high verification pulls up the score."""
        lstm_score = 0.48 # Uncertain/Slightly suspicious
        verification_score = 0.9 # Strong confirmation
        final_score, verdict, is_real = calculate_verdict(lstm_score, verification_score)
        
        self.assertTrue(is_real)
        self.assertEqual(verdict, "Likely Real News")
        self.assertGreater(final_score, 0.7)

    def test_verdict_logic_inconclusive(self):
        """Test the inconclusive range."""
        lstm_score = 0.5
        verification_score = 0.5
        final_score, verdict, is_real = calculate_verdict(lstm_score, verification_score)
        
        self.assertEqual(verdict, "Inconclusive / Mixed Evidence")

if __name__ == "__main__":
    unittest.main()
