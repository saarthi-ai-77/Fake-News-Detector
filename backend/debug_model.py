
import tensorflow as tf
from tensorflow.keras.models import load_model

def inspect():
    try:
        model = load_model("backend/fake_lstm_saved.keras")
        print("Model Layers:")
        for layer in model.layers:
             print(f"- {layer.name}: {layer.__class__.__name__}")
             if hasattr(layer, 'get_vocabulary'):
                 print(f"  Vocabulary size: {len(layer.get_vocabulary())}")
             if isinstance(layer, tf.keras.layers.TextVectorization):
                 print("  *** Contains TextVectorization ***")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
