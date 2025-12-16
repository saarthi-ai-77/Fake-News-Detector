
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import os

class FakeNewsModel:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.load()

    def load(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        
        print(f"Loading model from {self.model_path}...")
        try:
            self.model = load_model(self.model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            raise e

    def predict(self, text: str) -> float:
        if not self.model:
            raise ValueError("Model not loaded")
        
        # The model likely expects a specific input shape or string if TextVectorization is included.
        # If it's pure string input (TextVectorization inside model):
        try:
            # We pass a list/array of strings, but some models need tf.constant
            import tensorflow as tf
            input_data = tf.constant([text])
            pred = self.model.predict(input_data)
            return float(pred[0][0])
        except Exception as e:

            print(f"Prediction error: {e}")
            # Fallback if model expects tokenized input (unlikely if end-to-end but possible)
            # For now assume end-to-end with string input
            return 0.5  # Neutral fallback

# Singleton instance
model_path = os.path.join(os.path.dirname(__file__), "fake_lstm_saved.keras")
# If .keras doesn't work, we might fallback to .h5, but .keras is newer.
model_instance = None

def get_model():
    global model_instance
    if model_instance is None:
        model_instance = FakeNewsModel(model_path)
    return model_instance
