import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

model = tf.keras.models.load_model("./ml/Model_1Neuron_13Kernel_0.89accuracy")

img2 = load_img("./ml/visualisation/horizontal-offset-signal.png", target_size=(128, 128))
img = img_to_array(img2)
img = np.expand_dims(img, axis=0);

print(model.predict(img))

