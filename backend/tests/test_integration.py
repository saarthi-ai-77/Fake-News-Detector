
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch

client = TestClient(app)

def test_read_root_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_predict_text_empty():
    response = client.post("/predict-text", json={"text": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text cannot be empty"

def test_predict_text_real_input():
    # We mock verification to avoid API calls and model to avoid load time/consistency issues
    # Or we can test end-to-end if quota allows. Let's mock verification for stability.
    with patch("backend.main.verify_news") as mock_verify:
        mock_verify.return_value = (0.8, [{"name": "bbc.com", "url": "http://bbc.com", "trustScore": 1.0}])
        
        # We assume model is loaded real or fallback
        response = client.post("/predict-text", json={"text": "This is a credible news report."})
        assert response.status_code == 200
        data = response.json()
        assert "lstm_score" in data
        assert "verification_score" in data
        assert data["verification_score"] == 0.8
        assert len(data["matched_sources"]) == 1
        assert data["matched_sources"][0]["name"] == "bbc.com"

def test_predict_url_invalid():
    response = client.post("/predict-url", json={"url": ""})
    assert response.status_code == 400

@patch("backend.main.extract_text_from_url")
def test_predict_url_success(mock_extract):
    mock_extract.return_value = "Extracted content from URL"
    with patch("backend.main.verify_news") as mock_verify:
        mock_verify.return_value = (0.5, [])
        
        response = client.post("/predict-url", json={"url": "http://example.com/news"})
        assert response.status_code == 200
        data = response.json()
        assert data["verification_score"] == 0.5
        assert data["matched_sources"] == []

# Integration test without mocks (Warning: Uses Google API Quota)
# def test_live_integration():
#     response = client.post("/predict-text", json={"text": "Apple announces new iPhone features today."})
#     assert response.status_code == 200
#     data = response.json()
#     assert 0 <= data["final_score"] <= 1
