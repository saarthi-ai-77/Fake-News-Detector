
import os
import requests
from collections import Counter
import re
from urllib.parse import urlparse

# Load credentials
GOOGLE_API_KEY = ""
GOOGLE_CSE_ID = ""

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.txt")
if os.path.exists(CREDENTIALS_PATH):
    with open(CREDENTIALS_PATH, "r") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                if key == "GOOGLE_API_KEY":
                    GOOGLE_API_KEY = val
                elif key == "GOOGLE_CSE_ID":
                    GOOGLE_CSE_ID = val

TRUSTED_SOURCES = [
    "bbc.com", "reuters.com", "cnn.com", "nytimes.com", "washingtonpost.com",
    "theguardian.com", "aljazeera.com", "npr.org", "bloomberg.com", "forbes.com",
    "wsj.com", "usatoday.com", "apnews.com", "cnbc.com", "time.com",
    "nbcnews.com", "abcnews.go.com", "cbsnews.com", "foxnews.com", "msnbc.com",
    "huffpost.com", "economist.com", "financialexpress.com", "hindustantimes.com",
    "timesofindia.indiatimes.com", "indianexpress.com", "thehindu.com", "ndtv.com",
    "indiatoday.in", "livemint.com", "business-standard.com", "news18.com",
    "firstpost.com", "zeenews.india.com", "dnaindia.com", "outlookindia.com",
    "deccanherald.com", "telegraph.co.uk", "independent.co.uk", "standard.co.uk",
    "dailymail.co.uk", "mirror.co.uk", "sun.co.uk", "express.co.uk",
    "scmp.com", "straitstimes.com", "channelnewsasia.com", "dw.com", "france24.com",
    "euronews.com", "rt.com", "sputniknews.com", "chinadaily.com.cn", "xinhuanet.com"
]

FACT_CHECKER_SOURCES = [
    "snopes.com", "politifact.com", "factcheck.org", "fullfact.org", 
    "checkyourfact.com", "leadstories.com", "altnews.in", "boomlive.in"
]

FACT_CHECK_KEYWORDS = [
    "fact check", "fact-check", "debunk", "hoax", "false", 
    "fake news", "misleading", "correcting", "untrue", "unverified"
]

def extract_keywords(text: str, num_keywords: int = 5) -> str:
    """Improved keyword extraction using frequency and common word filtering."""
    text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    words = text_clean.split()
    
    stop_words = set([
        "the", "a", "an", "in", "on", "at", "for", "to", "of", "and", "or", "is", "are", "was", "were", 
        "it", "this", "that", "with", "by", "from", "be", "not", "have", "has", "had", "say", "said", "will",
        "would", "could", "should", "he", "she", "they", "we", "i", "you", "my", "his", "her", "their",
        "about", "as", "into", "like", "through", "after", "over", "between", "out", "against", "during",
        "without", "before", "under", "around", "among", "just", "very", "also", "been", "which"
    ])
    
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 3]
    most_common = Counter(meaningful_words).most_common(num_keywords)
    return " ".join([word for word, count in most_common])

def analyze_snippet(title: str, snippet: str) -> float:
    """
    Analyzes title and snippet for fact-checking sentiment.
    Returns a multiplier (0.0 to 1.5). 
    Low (< 1.0) means it's likely a debunk.
    High (> 1.0) means it's likely a confirmation.
    """
    content = (title + " " + snippet).lower()
    
    # Check for debunk keywords
    is_fact_check = any(kw in content for kw in FACT_CHECK_KEYWORDS)
    
    if is_fact_check:
        # If it says "false", "hoax", or "debunk", it's likely debunking the claim
        negative_indicators = ["false", "hoax", "debunk", "incorrect", "misleading", "fake"]
        if any(neg in content for neg in negative_indicators):
            return 0.1 # Strong negative signal
        return 0.5 # Weak negative signal
        
    return 1.2 # Likely a legitimate report or neutral mention

def verify_news(text: str):
    """
    Verifies news by searching Google and checking against trusted sources.
    Returns:
        score (float): 0.0 to 1.0
        matches (list): List of matching trusted domains found
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Google API credentials missing.")
        return 0.5, []

    keywords = extract_keywords(text)
    if not keywords:
        return 0.5, []

    print(f"Searching for: {keywords}")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": keywords,
        "num": 10
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        matches = []
        verdict_scores = []
        
        if "items" in data:
            for item in data["items"]:
                link = item.get("link", "")
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                domain = urlparse(link).netloc.lower()
                
                is_trusted = any(t in domain for t in TRUSTED_SOURCES)
                is_fact_checker = any(f in domain for f in FACT_CHECKER_SOURCES)
                
                if is_trusted or is_fact_checker:
                    sentiment_score = analyze_snippet(title, snippet)
                    
                    weight = 1.5 if is_fact_checker else 1.0
                    verdict_scores.append(sentiment_score * weight)
                    
                    matches.append({
                        "name": domain,
                        "url": link,
                        "trustScore": 1.0 if is_trusted else 1.2 # Fact checkers are high trust for debunking
                    })
        
        # Scoring Logic
        if not verdict_scores:
            # If no trusted sources found at all, score is low
            return 0.2, []

        # Average of verdict scores
        avg_verdict = sum(verdict_scores) / len(verdict_scores)
        
        # Normalize to 0-1
        # avg_verdict < 1 means mostly debunks, > 1 means support/neutral
        final_score = min(max(avg_verdict - 0.5, 0.0), 1.0) 
        
        # If we have a lot of debunks, force score down
        if any(s < 0.6 for s in verdict_scores):
             final_score = min(final_score, 0.3)

        # Deduplicate matches
        unique_matches = []
        seen_domains = set()
        for m in matches:
            if m["name"] not in seen_domains:
                unique_matches.append(m)
                seen_domains.add(m["name"])

        return float(final_score), unique_matches

    except Exception as e:
        print(f"Verification error: {e}")
        return 0.5, []
