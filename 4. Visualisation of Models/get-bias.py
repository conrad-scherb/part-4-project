import tensorflow as tf

model = tf.keras.models.load_model("./ml/Model_1Neuron_13Kernel_0.89accuracy")

for layer in model.layers:
    if (layer.name == 'dense'):
        print(layer.bias.numpy())