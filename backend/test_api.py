
import requests
import time

BASE_URL = "http://localhost:8000"

def test_text_prediction():
    print("Testing /predict-text...")
    payload = {
        "text": "The government announced a new tax policy today that affects small businesses. BBC reports that this is a significant change."
    }
    try:
        response = requests.post(f"{BASE_URL}/predict-text", json=payload)
        response.raise_for_status()
        data = response.json()
        print("Response:", data)
        assert "lstm_score" in data
        assert "verification_score" in data
        assert "final_score" in data
        assert "matched_sources" in data
        print("PASS /predict-text")
    except Exception as e:
        print(f"FAIL /predict-text: {e}")
        if 'response' in locals():
            print(response.text)

def test_url_prediction():
    print("\nTesting /predict-url...")
    # Use a real URL that is likely static or use a trusted source
    url = "https://www.bbc.com/news/world-60000000" # Might be 404, need a valid one or just check if it tries to fetch
    # Using a generic example that might exist or fail gracefully
    # Let's use something simple
    url = "https://www.example.com"
    
    payload = {"url": url}
    try:
        response = requests.post(f"{BASE_URL}/predict-url", json=payload)
        # It might fail extracting text if example.com is too simple or blocking, but let's see api response
        if response.status_code == 200:
            data = response.json()
            print("Response:", data)
            print("PASS /predict-url")
        else:
            print(f"Server returned {response.status_code}: {response.text}")
    except Exception as e:
        print(f"FAIL /predict-url: {e}")

if __name__ == "__main__":
    # Wait for server to come up if running in parallel, but here we run manually
    test_text_prediction()
    test_url_prediction()
