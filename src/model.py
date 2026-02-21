import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

MODEL = None
IMAGE_SIZE = (32, 32)

CLASS_LABELS = [
    "airplane","automobile","bird","cat","deer",
    "dog","frog","horse","ship","truck"
]

def load_model(model_path=None):
    global MODEL
    if MODEL is None:
        path = model_path if model_path else os.environ.get(
    "MODEL_PATH", "models/my_classifier_model.keras"
)
        MODEL = tf.keras.models.load_model(path)
    return MODEL

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMAGE_SIZE)
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def predict_image(preprocessed_image):
    model = load_model()
    predictions = model.predict(preprocessed_image)
    class_idx = np.argmax(predictions, axis=1)[0]

    return {
        "class_label": CLASS_LABELS[class_idx],
        "probabilities": predictions[0].tolist()
    }