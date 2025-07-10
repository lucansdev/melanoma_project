from abc import ABC, abstractmethod
from flask import Flask, jsonify, render_template, request,Response
import cv2
import tensorflow as tf
import keras
import numpy as np
import os

app = Flask(__name__)


class Image(ABC):
    def __init__(self, directory_image):
        self.directory_image = directory_image

    @abstractmethod
    def get_image(self):
        """
        This method should be implemented by subclasses to return an image tensor.
        """
        pass

class LoadImage(Image):
    def __init__(self, directory_image) -> None:
        super().__init__(directory_image)

    def get_image(self) -> tf.Tensor:
        image_stream = self.directory_image.read()
        image_array = np.frombuffer(image_stream, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise FileNotFoundError("Image could not be decoded. Please check the file format.")
        
        image_tensor = tf.convert_to_tensor(image, dtype=tf.float32) / 255.0
        image_tensor = tf.image.resize(image_tensor, (224, 224))
        image_tensor = tf.expand_dims(image_tensor, axis=0)

        return image_tensor

class Model(ABC):
    def __init__(self):
        self.model = None

    @abstractmethod
    def get_model(self, model_path) -> None:
        pass

    @abstractmethod
    def predict(self, image_tensor):
        pass

class JeramyModel(Model):
    def __init__(self):
        super().__init__()

    def get_model(self, model_path) -> None:
        if not os.path.exists(model_path):
             raise FileNotFoundError(f"Model not found at the specified path: {model_path}")
        try:
            self.model = keras.models.load_model(model_path)
            lr = tf.keras.optimizers.schedules.ExponentialDecay(initial_learning_rate=1e-3, decay_steps=10000, decay_rate=0.9)
            adam = tf.keras.optimizers.Adam(learning_rate=lr)
            self.model.compile(optimizer=adam, loss="binary_crossentropy", metrics=["accuracy"])
            print("--- Model Loaded and Compiled Successfully ---") 
        except Exception as e:
            raise IOError(f"Error loading the model: {e}")

    def predict(self, image_tensor):
        if not isinstance(image_tensor, tf.Tensor):
            raise TypeError("Image is not a tensor")
        
        if self.model is None:
            raise ValueError("Model is not loaded")
        
        prediction = self.model.predict(image_tensor)
        return prediction.tolist()
    

model_path = "/home/lucas/Área de Trabalho/project_ai/cancer_project/model/cancer_model.h5"
melanoma_model = JeramyModel()
melanoma_model.get_model(model_path)


@app.route("/")
def render_welcome():
    return render_template("index.html")

@app.route("/teste", methods=["GET", "POST"])
def predict_cancer():
    if request.method == "GET":
        return render_template("test.html")
    

    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        try:
            image_loader = LoadImage(file)
            image_tensor = image_loader.get_image()
            prediction = melanoma_model.predict(image_tensor)
            acc = 0
            if prediction[0][0] >= 0.5:
                acc = prediction[0][0] * 100
            else:
                acc = (1- prediction[0][0]) * 100

            return jsonify({"response": prediction,"acc":acc})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/resultado")
def resultado():
    return render_template("resultado.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False,host="0.0.0.0")