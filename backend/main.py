
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

try:
    from backend.model import get_model
    from backend.verify import verify_news
    from backend.utils import extract_text_from_url
except ImportError:
    from model import get_model
    from verify import verify_news
    from utils import extract_text_from_url

app = FastAPI(title="Fake News Detection API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TextRequest(BaseModel):
    text: str

class UrlRequest(BaseModel):
    url: str

class Source(BaseModel):
    name: str
    url: str
    trustScore: Optional[float] = 1.0

class PredictionResponse(BaseModel):
    lstm_score: float
    verification_score: float
    final_score: float
    verdict: str
    matched_sources: List[Source]
    is_real: bool

def calculate_verdict(lstm_score, verification_score):
    # final_score = (0.7 * lstm_score) + (0.3 * verification_score)
    # NOTE: LSTM usually outputs probability of being "Fake" (1) or "Real" (0), or vice versa.
    # We need to know what the model output means.
    # Usually 1 = Fake, 0 = Real in many datasets, OR 1 = Real, 0 = Fake.
    # The prompt says: "Output real_news_probability (0–1)" for LSTM. 
    # So I will assume output is P(Real).
    
    # Adjusted Logic:
    # Since LSTM is hovering around 0.5 (neutral/uncertain), we need to rely more on verification.
    # If Verification is high (>0.8), it should pull the score up significantly.
    # If Verification is low (<0.3), it should pull it down.
    
    # Weight: 60% Verification, 40% LSTM
    final_score = (0.4 * lstm_score) + (0.6 * verification_score)
    
    # Threshold: 0.5
    is_real = final_score >= 0.5
    verdict = "Likely Real News" if is_real else "Likely Fake News"
    return final_score, verdict, is_real

@app.post("/predict-text", response_model=PredictionResponse)
async def predict_text(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # 1. LSTM Prediction
    try:
        model = get_model()
        lstm_score = model.predict(request.text) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    # 2. Verification
    verification_score, matches = verify_news(request.text)

    # 3. Final Logic
    final_score, verdict, is_real = calculate_verdict(lstm_score, verification_score)

    sources = [Source(**m) for m in matches]

    return PredictionResponse(
        lstm_score=lstm_score,
        verification_score=verification_score,
        final_score=final_score,
        verdict=verdict,
        matched_sources=sources,
        is_real=is_real
    )

@app.post("/predict-url", response_model=PredictionResponse)
async def predict_url(request: UrlRequest):
    if not request.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # 1. Fetch content
    text = extract_text_from_url(request.url)
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from URL")

    # Re-use logic (could refactor, but keeping simple)
    # 2. LSTM
    try:
        model = get_model()
        lstm_score = model.predict(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    # 3. Verification
    verification_score, matches = verify_news(text)

    # 4. Final Logic
    final_score, verdict, is_real = calculate_verdict(lstm_score, verification_score)
    
    sources = [Source(**m) for m in matches]

    return PredictionResponse(
        lstm_score=lstm_score,
        verification_score=verification_score,
        final_score=final_score,
        verdict=verdict,
        matched_sources=sources,
        is_real=is_real
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
