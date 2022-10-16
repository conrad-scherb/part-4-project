import tensorflow as tf

LAYER_NAME = "./ml/Model_1Neuron_13Kernel_0.89accuracy"
LAYER_TYPE = "dense"

model = tf.keras.models.load_model(LAYER_NAME)

for layer in model.layers:
    if (layer.name == LAYER_TYPE):
        print(layer.bias.numpy())