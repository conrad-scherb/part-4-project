from cmath import nan
import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
from random import seed
from random import randint
from sklearn.model_selection import KFold

import matplotlib.pyplot as plt

#Limit the number of memory used for GPU
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
print("TensorFlow version:", tf.__version__)
GPU_Device = tf.config.experimental.list_physical_devices('GPU')
print("Num GPUs Available: ", len(GPU_Device))
tf.config.experimental.set_memory_growth(GPU_Device[0], True)
#os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

#Go to the directory with the data
data_dir = pathlib.Path("../DataGenerationUpdated/UserDataTraining/")

#Determining Seed
seed = randint(0, 5000)
print("The seed for this run is: ", seed)
epochs = 1000

#Training data
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.1,
    subset="training",
    seed = seed,
    image_size=(128, 128),
    batch_size=32)

#Validation data
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.1,
    subset="validation",
    seed = seed,
    image_size=(128, 128),
    batch_size=32)

#Data augmentation to reduce overfitting
data_augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomFlip("vertical"),
    ]
)

#Callback to stop model after plateu has been reached
class plateuStop(tf.keras.callbacks.Callback):
    def __init__(self):
        super(plateuStop, self).__init__()
        self.accuracies = list()
        self.losses = list()

    def accuracyPlateu(self):
        #Check the last 10 values of the has crateed a new maximum
        if len(self.accuracies) < 200:
            return False
        if (max(self.accuracies[-20:]) < max(self.accuracies)):
            return True
        else:
            return False

    def onCompletion(self):
        #Calculate Epochs until plateu
        accuracies = np.array(self.accuracies)
        losses = np.array(self.losses)
        print("Number of epochs until plateau: ", len(self.accuracies))
        print("The mean plateau value accuract is: ", np.mean(accuracies[np.argpartition(self.accuracies, -10)[-10:].astype(int)]))  #Taking the top 6 elements mean
        print("The mean plateau value loss is: ", np.mean(losses[np.argpartition(self.accuracies, -10)[-10:]]))
        print("The mean plateau value STD is: ", np.std(accuracies[np.argpartition(self.accuracies, -10)[-10:]]))

    def on_epoch_end(self, epoch, logs=None):
        self.accuracies.append(logs["val_accuracy"])
        self.losses.append(logs["val_loss"])
        #Check for error where val accuracy not increasing at all
        if (len(self.accuracies) > 50) & (len(set(self.accuracies[-100:])) <= 1):
            self.model.stop_training = True
        if (self.accuracyPlateu() | (len(self.accuracies)==epochs)):
            self.onCompletion()
            self.model.stop_training = True

#Normalising the images to within 0:1
normalization_layer = tf.keras.layers.Rescaling(1./255)

#Structure of the model
model = tf.keras.Sequential([
  data_augmentation,
  normalization_layer,
  tf.keras.layers.Conv2D(1,13, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dropout(0.25),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

#Compile the model
model.compile(
    optimizer= tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.0, nesterov=False, name="SGD"),
    loss='binary_crossentropy',
    metrics=['accuracy'])

#print("Number of training inputs", len(inputs[train]))
#print("Number of training input labels", len(targets[train]))

#print("Number of testing inputs", len(inputs[test]))
#print("Number of testing input labels", len(targets[test]))

#Fit the model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    batch_size=64,
    callbacks = [plateuStop()]
)

#Save the model
val_acc = history.history['val_accuracy']
model.save("Model_1Neuron_13Kernel_" +  str(round(val_acc[len(val_acc)-1], 2)) + "accuracy") 