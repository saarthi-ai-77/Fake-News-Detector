
import requests
import json

BASE_URL = "http://localhost:8000/predict-text"

def test_news(text, label):
    print(f"--- Testing {label} News ---")
    print(f"Text: {text[:100]}...")
    try:
        response = requests.post(BASE_URL, json={"text": text})
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    print("\n")

if __name__ == "__main__":
    # Real News 1
    real1 = "The James Webb Space Telescope has captured new images of the Pillars of Creation, revealing more detail about star formation in the Eagle Nebula. NASA released the high-resolution infrared credibility today."
    test_news(real1, "REAL")

    # Real News 2
    real2 = "The World Health Organization has declared the end of the global health emergency for mpox, citing a significant decline in reported cases worldwide over the past few months."
    test_news(real2, "REAL")

    # Fake News 1
    fake1 = "BREAKING: The moon has been confirmed to be a hollow spaceship placed by ancient aliens. Top government officials have been hiding this secret for 50 years!"
    test_news(fake1, "FAKE")

    # Fake News 2
    fake2 = "Doctors are baffled by this one weird trick! Drinking 5 gallons of salt water every morning cures cancer and makes you immortal instantly. Big Pharma hates this!"
    test_news(fake2, "FAKE")
