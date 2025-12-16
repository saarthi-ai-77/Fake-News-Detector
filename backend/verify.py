
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
    "bbc.com",
    "reuters.com",
    "cnn.com",
    "thehindu.com",
    "nytimes.com",
    "indianexpress.com"
]

def extract_keywords(text: str, num_keywords: int = 5) -> str:
    # Simple extraction: remove short words, count frequency
    words = re.findall(r'\w+', text.lower())
    # Filter common stop words (very basic list)
    stop_words = set([
        "the", "a", "an", "in", "on", "at", "for", "to", "of", "and", "or", "is", "are", "was", "were", 
        "it", "this", "that", "with", "by", "from", "be", "not", "have", "has", "had", "say", "said", "will"
    ])
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    most_common = Counter(meaningful_words).most_common(num_keywords)
    return " ".join([word for word, count in most_common])

def verify_news(text: str):
    """
    Verifies news by searching Google and checking against trusted sources.
    Returns:
        score (float): 0.0 to 1.0 (1.0 = highly verified)
        matches (list): List of matching trusted domains found
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Google API credentials missing.")
        return 0.0, []

    keywords = extract_keywords(text)
    if not keywords:
        return 0.0, []

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
        
        if "items" not in data:
            return 0.0, []

        matches = []
        for item in data["items"]:
            link = item.get("link", "")
            domain = urlparse(link).netloc.lower()
            # Handle "www.bbc.com" -> match "bbc.com"
            for trusted in TRUSTED_SOURCES:
                if trusted in domain:
                    matches.append({
                        "name": trusted, # using domain as name for now
                        "url": link,
                        "trustScore": 1.0
                    })
                    break
        
        # Calculate score: matched_trusted / total_results (capped at 1.0? or just ratio)
        # Prompt says: verification_score = trusted_matches / total_results
        # But wait, total_results returned by API (e.g. 10)
        
        matches_count = len(matches)
        total_results = len(data["items"]) # usually 10
        
        score = matches_count / total_results if total_results > 0 else 0.0
        
        # Deduplicate matches for display
        unique_matches = []
        seen_urls = set()
        for m in matches:
            if m["url"] not in seen_urls:
                unique_matches.append(m)
                seen_urls.add(m["url"])

        return score, unique_matches

    except Exception as e:
        print(f"Verification error: {e}")
        return 0.0, []
