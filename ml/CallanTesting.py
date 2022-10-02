from cmath import nan
import numpy as np
import os
import gc
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
data_dir = pathlib.Path("../DataGenerationUpdated/UserDataTrainingSmall/")

#Determining Seed
seed = randint(0, 5000)
print("The seed for this run is: ", seed)
epochs = 1000

#Training data
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    seed = seed,
    shuffle=False,
    #image_size=(150, 150)) #Large
    #image_size=(128, 128)) #Medium
    image_size=(106, 106)) #Small

#Convert into npy arrays 
inputs = np.concatenate(list(train_ds.map(lambda x, y:x)))
targets = np.concatenate(list(train_ds.map(lambda x, y:y)))

#Implementing K-Fold cross validation
num_folds = 10
platacc_per_fold = []
platstd_per_fold = []
plattime_per_fold = []
platloss_per_fold = []
kfold = KFold(n_splits=num_folds, shuffle=True)

#Run through the splits
fold_no = 1
for train, test in kfold.split(inputs, targets):
    
    # Generate a print
    print('------------------------------------------------------------------------')
    print(f'Training for fold {fold_no} ...')
    
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
            if len(self.accuracies) < 350:
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
            platacc_per_fold.append(np.mean(accuracies[np.argpartition(self.accuracies, -10)[-10:]]))
            platstd_per_fold.append(np.std(accuracies[np.argpartition(self.accuracies, -10)[-10:]]))
            plattime_per_fold.append(len(self.accuracies))
            platloss_per_fold.append(np.mean(losses[np.argpartition(self.accuracies, -10)[-10:]]))

        def on_epoch_end(self, epoch, logs=None):
            self.accuracies.append(logs["val_accuracy"])
            self.losses.append(logs["val_loss"])
            #Check for error where val accuracy not increasing at all
            if (len(self.accuracies) > 40) & (len(set(self.accuracies[-100:])) <= 1):
                self.model.stop_training = True
                platacc_per_fold.append(np.nan)
                platstd_per_fold.append(np.nan)
                plattime_per_fold.append(np.nan)
                platloss_per_fold.append(np.nan)
            if (self.accuracyPlateu() | (len(self.accuracies)==epochs)):
                self.onCompletion()
                self.model.stop_training = True

    #Normalising the images to within 0:1
    normalization_layer = tf.keras.layers.Rescaling(1./255)

    #Structure of the model
    model = tf.keras.Sequential([
      data_augmentation,
      normalization_layer,
      tf.keras.layers.Conv2D(32, 13), 
      tf.keras.layers.LeakyReLU(alpha=0.1),
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
      inputs[train], 
      targets[train],
      validation_data=(inputs[test], targets[test]),
      epochs=epochs,
      batch_size=64,
      callbacks = [plateuStop()]
    )

    # Increase fold number
    fold_no = fold_no + 1
    gc.collect()

#Post final statistics of the model
print('------------------------------------------------------------------------')
print('Score per fold')
for i in range(0, len(platacc_per_fold)):
  print('------------------------------------------------------------------------')
  print(f'> Fold {i+1} - Loss: {platloss_per_fold[i]} - Accuracy: {platacc_per_fold[i]}% - Epochs: {plattime_per_fold[i]}')
print('------------------------------------------------------------------------')
print('Average scores for all folds:')
print(f'> Accuracy: {np.nanmean(platacc_per_fold)} (+- {np.nanstd(platacc_per_fold)})')
print(f'> Loss: {np.nanmean(platloss_per_fold)} (+- {np.nanstd(platloss_per_fold)})')
print(f'> Epochs: {np.nanmean(plattime_per_fold)} (+- {np.nanstd(plattime_per_fold)})')
print('------------------------------------------------------------------------')

#Atetmpting to generate the 
#pred = model.predict(
#    validation_ds,
#    batch_size=4)
#pred = tf.greater(pred, 0.5)
#print(pred)
#labels = np.concatenate([y for x, y in validation_ds], axis = 0)
#print(labels)
#print(tf.math.confusion_matrix(labels, pred))

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