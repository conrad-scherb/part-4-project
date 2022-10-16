import tensorflow as tf
import numpy as np
from matplotlib import pyplot
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configurable Parmeters
MODEL_PATH = "../Model_32-16Neuron_5-13Kernel_0.956accuracy"
LAYER_NAME = "conv2d/kernel:0"
IMAGE_LIST = [
	"../../DataGenerationUpdated/OffsetTestImages/AllAngles.png",
	"../../DataGenerationUpdated/UserDataTraining/UserNoSignal/PilotData2_Result=110.png",
	"../../DataGenerationUpdated/UserDataTraining/UserSignal/PilotData17_Result=121.png"
]

# Main Script Body

model = tf.keras.models.load_model(MODEL_PATH)

# Plot convolutional kernels
filters = [v for v in model.trainable_variables if v.name == LAYER_NAME][0].numpy()

# Slice filters if too large
#filters = filters.slice(16)

f_min, f_max = filters.min(), filters.max()

# Comment this in/out to turn on/off rescaling of filter params
##filters = (filters - f_min) / (f_max - f_min)

n_filters, ix = filters.shape[3], 2

SUBPLOT_ROWS = len(IMAGE_LIST) + 1
SUBPLOT_COLS = n_filters + 1

for i in range(6):
	f = filters[:, :, :, i]
	ax = pyplot.subplot(SUBPLOT_ROWS, SUBPLOT_COLS, ix)
	ax.set_xticks([])
	ax.set_yticks([])
	pyplot.imshow(f[:, :, 1], cmap='gray')
	ix += 1;

for IMAGE_PATH in IMAGE_LIST:
	untransformed_img = load_img(IMAGE_PATH, target_size=(128, 128))
	img = img_to_array(untransformed_img)
	img = np.expand_dims(img, axis=0);

	output = model.layers[2].output
	model_quick = tf.keras.Model(inputs=model.inputs, outputs=output)

	feature_output = model_quick.predict(img)

	ax = pyplot.subplot(SUBPLOT_ROWS, SUBPLOT_COLS, ix)
	ax.set_xticks([])
	ax.set_yticks([])
	pyplot.imshow(untransformed_img, cmap='gray')
	ix += 1;

	for ftr in range(6):
		ax = pyplot.subplot(2, 7, ix)
		ax.set_xticks([])
		ax.set_yticks([])
		pyplot.imshow(feature_output[0, :, :, ftr], cmap='gray')
		ix += 1;

pyplot.show()
