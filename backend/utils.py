import requests
from bs4 import BeautifulSoup
import re

def extract_text_from_url(url: str) -> str:
    """
    Fetches the content of a URL and extracts the main text.
    Returns the title + text content.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Kill all script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        title = soup.title.string if soup.title else ""
        
        return f"{title}\n\n{text}"[:5000] # Limit to 5000 chars to avoid overloading model
        
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""
