import tensorflow as tf
import pathlib
from random import randint

model = tf.keras.models.load_model("../Model_8Neuron_13Kernel_0.93accuracy")

data_dir = pathlib.Path("../../DataGenerationUpdated/RandomOffsetData/")

#Determining Seed
seed = randint(0, 5000)
print("The seed for this run is: ", seed)

dataset = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    seed = seed,
    shuffle=False,
    image_size=(128, 128)) 

print(model.evaluate(dataset))