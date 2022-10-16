import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = tf.keras.models.load_model("./ml/Model_1Neuron_13Kernel_0.89accuracy")

img2 = load_img("./DataGenerationUpdated/diagonal.png", target_size=(128, 128))
img = img_to_array(img2)
img = np.expand_dims(img, axis=0);

print(model.predict(img))

