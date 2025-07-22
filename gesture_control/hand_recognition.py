import cv2
import numpy as np
from keras.models import load_model

CLASSES = ["Luzes", "Portas", "Clima"]

class HandRecognizer:
    def __init__(self, model_path='Keras Hands/keras_model.h5'):
        try:
            self.model = load_model(model_path)
            print("Modelo carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar o modelo: {e}")
            raise e
        self.input_data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    def predict_gesture(self, frame, y_min, y_max, x_min, x_max, counter):
        cropped = frame[y_min - 50:y_max + 50, x_min - 50:x_max + 50]
        resized = cv2.resize(cropped, (224, 224))
        normalized = (resized.astype(np.float32) / 127.0) - 1
        self.input_data[0] = normalized
        prediction = self.model.predict(self.input_data)
        index = np.argmax(prediction)
        gesture = CLASSES[index]
        return gesture, counter
