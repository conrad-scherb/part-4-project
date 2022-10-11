import tensorflow as tf
import numpy as np
from matplotlib import pyplot
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = tf.keras.models.load_model("./ml/Model_4Neuron_13Kernel")

# Plot convolutional kernels
filters = [v for v in model.trainable_variables if v.name == "conv2d/kernel:0"][0].numpy()


f_min, f_max = filters.min(), filters.max()
##filters = (filters - f_min) / (f_max - f_min)
n_filters, ix = filters.shape[3], 2

for i in range(n_filters):
	f = filters[:, :, :, i]
	ax = pyplot.subplot(4, n_filters+1, ix)
	ax.set_xticks([])
	ax.set_yticks([])
	pyplot.imshow(f[:, :, 1], cmap='gray')
	ix += 1

# Do it again with all angles image
untransformed_img = load_img("../../DataGenerationUpdated/OffsetTestImages/AllAngles.png", target_size=(128, 128))
img = img_to_array(untransformed_img)
img = np.expand_dims(img, axis=0);

output = model.layers[2].output
model_quick = tf.keras.Model(inputs=model.inputs, outputs=output)

feature_output = model_quick.predict(img)

ax = pyplot.subplot(4, n_filters+1, ix)
ax.set_xticks([])
ax.set_yticks([])
pyplot.imshow(untransformed_img, cmap='gray')
ix += 1;

for ftr in range(feature_output.shape[3]):
    ax = pyplot.subplot(4, n_filters+1, ix)
    ax.set_xticks([])
    ax.set_yticks([])
    pyplot.imshow(feature_output[0, :, :, ftr], cmap='gray')
    ix += 1;

# Plot the output of the convolutional layers with a non-signal image
untransformed_img = load_img("./DataGenerationUpdated/UserDataTraining/UserNoSignal/PilotData2_Result=110.png", target_size=(128, 128))
img = img_to_array(untransformed_img)
img = np.expand_dims(img, axis=0);

output = model.layers[2].output
model_quick = tf.keras.Model(inputs=model.inputs, outputs=output)

feature_output = model_quick.predict(img)

ax = pyplot.subplot(4, n_filters+1, ix)
ax.set_xticks([])
ax.set_yticks([])
pyplot.imshow(untransformed_img, cmap='gray')
ix += 1;

for ftr in range(feature_output.shape[3]):
    ax = pyplot.subplot(4, n_filters+1, ix)
    ax.set_xticks([])
    ax.set_yticks([])
    pyplot.imshow(feature_output[0, :, :, ftr], cmap='gray')
    ix += 1;

# Do it again with a signal image
untransformed_img = load_img("./DataGenerationUpdated/diagonal.png", target_size=(128, 128))
img = img_to_array(untransformed_img)
img = np.expand_dims(img, axis=0);

output = model.layers[2].output
model_quick = tf.keras.Model(inputs=model.inputs, outputs=output)

feature_output = model_quick.predict(img)

ax = pyplot.subplot(4, n_filters+1, ix)
ax.set_xticks([])
ax.set_yticks([])
pyplot.imshow(untransformed_img, cmap='gray')
ix += 1;

for ftr in range(feature_output.shape[3]):
    ax = pyplot.subplot(4, n_filters+1, ix)
    ax.set_xticks([])
    ax.set_yticks([])
    pyplot.imshow(feature_output[0, :, :, ftr], cmap='gray')
    ix += 1;

pyplot.show()
