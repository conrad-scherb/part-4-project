import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
from random import seed
from random import randint

#Limit the number of memory used for GPU
print("TensorFlow version:", tf.__version__)
GPU_Device = tf.config.experimental.list_physical_devices('GPU')
print("Num GPUs Available: ", len(GPU_Device))
tf.config.experimental.set_memory_growth(GPU_Device[0], True)

#Go to the directory with the data
data_dir = pathlib.Path("../DataGenerationUpdated/UserDataTraining/")

#Mark the dataset as the png images from the files
list_ds = tf.data.Dataset.list_files(str(data_dir/"*/*.png"))

#Indicate the negative dataset
nosignal = list(data_dir.glob('UserNoSignal/*'))
PIL.Image.open(str(nosignal[0]))

#Determining Seed
seed = randint(0, 5000)
print("The seed for this run is: ", seed)

#Training data
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed = seed,
    image_size=(768, 768),
    batch_size=4)

#Validation data
validation_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed = seed,
    image_size=(768, 768),
    batch_size=4)

#Data augmentation to reduce overfitting
data_augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal"),
    ]
)

#Normalising the images to within 0:1
normalization_layer = tf.keras.layers.Rescaling(1./255)

#Structure of the model
model = tf.keras.Sequential([
  #data_augmentation,
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(64, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(16, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.5),
  tf.keras.layers.Dense(2)
])

model.compile(
  optimizer= tf.keras.optimizers.Adam(learning_rate=0.5e-3),
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

model.fit(
  train_ds,
  validation_data=validation_ds,
  epochs=10
)