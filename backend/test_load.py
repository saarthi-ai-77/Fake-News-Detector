
import os
import tensorflow as tf
from tensorflow.keras.models import load_model

def inspect(path):
    print(f"Loading {path}...")
    try:
        model = load_model(path)
        model.summary()
        for layer in model.layers:
            if isinstance(layer, tf.keras.layers.TextVectorization):
                print("Found TextVectorization layer")
                return
        print("No TextVectorization layer found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect("d:/FND-LSTM/backend/fake_lstm_saved.keras")
    inspect("d:/FND-LSTM/backend/best_lstm.h5")
