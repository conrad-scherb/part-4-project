import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib

data_dir = pathlib.Path("../DataGenerationUpdated/BaseData/")
list_ds = tf.data.Dataset.list_files(str(data_dir/"*/*.png"))

nosignal = list(data_dir.glob('NoSignal/*'))
PIL.Image.open(str(nosignal[0]))

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=642524,
    image_size=(256, 256),
    batch_size=8)

validation_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=642524,
    image_size=(256, 256),
    batch_size=8)

normalization_layer = tf.keras.layers.Rescaling(1./255)

model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation="relu"),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation="relu"),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.5),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)

model.compile(
  optimizer=tf.keras.optimizers.SGD(), #SGD
  loss='binary_crossentropy',
  metrics='accuracy')

model.fit(
  train_ds,
  validation_data=validation_ds,
  epochs=20,
  callbacks=[reduce_lr]
)

model.evaluate(validation_ds)