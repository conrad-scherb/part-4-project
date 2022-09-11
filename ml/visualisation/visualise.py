import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import numpy as np

model = tf.keras.models.load_model("./ml/Model_4Neuron_13Kernel")

for v in model.trainable_variables:
    print(v.name)

filters = [v for v in model.trainable_variables if v.name == "conv2d/kernel:0"][0]
print(filters.shape)

for f in range(filters.shape[3]):
    print(filters[:, :, 1, f])

output = model.layers[2].output
model_quick = tf.keras.Model(inputs=model.inputs, outputs=output)

img2 = load_img("./DataGenerationUpdated/UserDataTraining/UserSignal/lisa.png", target_size=(128, 128))
img = img_to_array(img2)
img = np.expand_dims(img, axis=0);

feature_output = model_quick.predict(img)

columns = 4
rows = 1
for ftr in feature_output:
    #pos = 1
    fig=plt.figure(figsize=(40, 40))
    fig =plt.subplot(1, 5, 1)
    plt.imshow(img2, cmap='gray')
    for i in range(2, columns*rows +2):
        fig =plt.subplot(rows, columns+1, i)
        fig.set_xticks([])  #Turn off axis
        fig.set_yticks([])
        plt.imshow(ftr[:, :, i-2], cmap='gray')
        #pos += 1
    plt.show()

