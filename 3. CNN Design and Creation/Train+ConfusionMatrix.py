import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
from random import seed
from random import randint

import matplotlib.pyplot as plt

#Limit the number of memory used for GPU
print("TensorFlow version:", tf.__version__)
GPU_Device = tf.config.experimental.list_physical_devices('GPU')
print("Num GPUs Available: ", len(GPU_Device))
tf.config.experimental.set_memory_growth(GPU_Device[0], True)

#Go to the directory with the data
data_dir = pathlib.Path("../DataGenerationUpdated/BaseData/") #NOTE: WIll NEED TO CHNAGE DEPEDNING ON WHERE IMAGES ARE STORED

#Mark the dataset as the png images from the files
list_ds = tf.data.Dataset.list_files(str(data_dir/"*/*.png"))

#Indicate the negative dataset
nosignal = list(data_dir.glob('NoSignal/*'))
PIL.Image.open(str(nosignal[0]))

#Determining Seed
#seed = 642524
seed = randint(0, 5000)
print("The seed for this run is: ", seed)
epochs = 10

#Training data
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed = seed,
    image_size=(256, 256),
    batch_size=4)

#Validation data
validation_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed = seed,
    image_size=(256, 256),
    batch_size=4)

#Data augmentation to reduce overfitting
data_augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomFlip("vertical"),
    ]
)

#Normalising the images to within 0:1
normalization_layer = tf.keras.layers.Rescaling(1./255)

#Structure of the model
model = tf.keras.Sequential([ #XCHANGE THIS TO CHNAGE THE STRUCTURE OF THE MODEL
  data_augmentation,
  normalization_layer,
  tf.keras.layers.Conv2D(64, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.25),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

#Compiles the model to prepare it for train ing
model.compile(
  optimizer= tf.keras.optimizers.Adam(learning_rate=0.5e-3),
  loss='binary_crossentropy',
  metrics=['accuracy'])

#FItting and training the model
history = model.fit(
  train_ds,
  validation_data=validation_ds,
  epochs=epochs,
)

#Prediction Data
data_dir = pathlib.Path("../DataGenerationUpdated/ConfusionMatrixData/")
prediction_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    seed = seed,
    shuffle=False,
    image_size=(256, 256),
    batch_size=1)

#Atetmpting to generate the confusion matrix
pred = model.predict(
    prediction_ds)
pred = tf.greater(pred, 0.5)
print(pred)
labels = np.concatenate([y for x, y in prediction_ds], axis = 0)
print(labels)
print(tf.math.confusion_matrix(labels, pred))

#Plotting results of model
#acc = history.history['accuracy']
#val_acc = history.history['val_accuracy']
#loss = history.history['loss']
#val_loss = history.history['val_loss']

#plt.plot(acc, 'bo', label='Training acc')
#plt.plot(val_acc, 'b', label='Validation acc')
#plt.title('Training and validation accuracy')
#plt.legend()

#plt.figure()

#plt.plot(loss, 'bo', label='Training loss')
#plt.plot(val_loss, 'b', label='Validation loss')
#plt.title('Training and validation loss')
#plt.legend()

#plt.show()