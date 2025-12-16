
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

def extract_keywords(text: str, num_keywords: int = 5) -> str:
    # Improved keyword extraction
    # Remove special chars but keep spaces
    text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    words = text_clean.split()
    
    stop_words = set([
        "the", "a", "an", "in", "on", "at", "for", "to", "of", "and", "or", "is", "are", "was", "were", 
        "it", "this", "that", "with", "by", "from", "be", "not", "have", "has", "had", "say", "said", "will",
        "would", "could", "should", "he", "she", "they", "we", "i", "you", "my", "his", "her", "their",
        "about", "as", "into", "like", "through", "after", "over", "between", "out", "against", "during",
        "without", "before", "under", "around", "among"
    ])
    
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Prioritize proper nouns (capitalized in original text) - simple heuristic
    # (Not implemented here to keep it simple, relying on freq)
    
    most_common = Counter(meaningful_words).most_common(num_keywords)
    return " ".join([word for word, count in most_common])

def verify_news(text: str):
    """
    Verifies news by searching Google and checking against trusted sources.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Google API credentials missing.")
        return 0.5, [] # Neutral score if no API

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
        if "items" in data:
            for item in data["items"]:
                link = item.get("link", "")
                domain = urlparse(link).netloc.lower()
                
                # Check for substring match in trusted list
                for trusted in TRUSTED_SOURCES:
                    if trusted in domain:
                        matches.append({
                            "name": trusted,
                            "url": link,
                            "trustScore": 1.0
                        })
                        break
        
        # Scoring Logic
        # If we find ANY trusted source reporting this, it's likely real.
        # Score = 1.0 if any match, else 0.0? 
        # Let's retain a bit of nuance.
        
        matches_count = len(matches)
        
        if matches_count > 0:
            # High confidence if verified sources found
            score = 0.8 + (min(matches_count, 2) * 0.1) # 1 match = 0.9, 2+ = 1.0
            if score > 1.0: score = 1.0
        else:
            # If no matches found in trusted sources, it is suspicious
            # BUT efficient keywords might fail.
            # Let's give a small penalty but not 0
            score = 0.2
            
        # Deduplicate matches
        unique_matches = []
        seen_urls = set()
        for m in matches:
            if m["url"] not in seen_urls:
                unique_matches.append(m)
                seen_urls.add(m["url"])

        return score, unique_matches

    except Exception as e:
        print(f"Verification error: {e}")
        return 0.5, []

