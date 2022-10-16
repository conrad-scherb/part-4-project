import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configurable Parmeters
MODEL_PATH = "./ml/Model_1Neuron_13Kernel_0.89accuracy"
IMAGE_PATH = "./DataGenerationUpdated/diagonal.png"

# Main Script Body
model = tf.keras.models.load_model(MODEL_PATH)

img2 = load_img(IMAGE_PATH, target_size=(128, 128))
img = img_to_array(img2)
img = np.expand_dims(img, axis=0);

print(model.predict(img))

