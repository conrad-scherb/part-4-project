import tensorflow as tf
from matplotlib import pyplot
model = tf.keras.models.load_model("./ml/Model_4Neuron_17Kernel")

filters = [v for v in model.trainable_variables if v.name == "conv2d/kernel:0"][0].numpy()

f_min, f_max = filters.min(), filters.max()
filters = (filters - f_min) / (f_max - f_min)
n_filters, ix = 4, 1
for i in range(n_filters):
	f = filters[:, :, :, i]
	for j in range(3):
		ax = pyplot.subplot(n_filters, 3, ix)
		ax.set_xticks([])
		ax.set_yticks([])
		pyplot.imshow(f[:, :, j], cmap='gray')
		ix += 1
pyplot.show()