import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import matplotlib.pyplot as plt

model = tf.keras.models.load_model("./ml/Model_32Neuron_9Kernel")

for v in model.trainable_variables:
    print(v.name)

filters = [v for v in model.trainable_variables if v.name == "conv2d/kernel:0"][0]
print(filters.shape)

for f in range(filters.shape[3]):
    print(filters[:, :, 1, f])

output = model.layers[2].output
model_quick = tf.keras.Model(inputs=model.inputs, outputs=output)

img = load_img("./DataGenerationUpdated/UserDataTraining/UserNoSignal/PilotData2_Result=110.png", target_size=(128, 128))
img = img_to_array(img)
img = np.expand_dims(img, axis=0);

feature_output = model_quick.predict(img)

columns = 8
rows = 4
for ftr in feature_output:
    #pos = 1
    fig=plt.figure(figsize=(40, 40))
    for i in range(1, columns*rows +1):
        fig =plt.subplot(rows, columns, i)
        fig.set_xticks([])  #Turn off axis
        fig.set_yticks([])
        plt.imshow(ftr[:, :, i-1], cmap='gray')
        #pos += 1
    plt.show()

