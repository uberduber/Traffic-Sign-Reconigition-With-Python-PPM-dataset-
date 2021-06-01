# -*- coding: utf-8 -*-
"""Phân loại biển báo giao thông với GUI (dùng tệp PPM)  .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16ZlOaaZl472Bpf5vam8FWnUZyvvb8Hio

khởi tạo và import thư viện
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image 
import os
from glob import glob
import PIL.Image as Image

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

"""DATASET PNG GGDRIVE ( TRONG PACK NÀY CÓ BAO GỒM file TEST.CSV)
Dùng kiểm giá trị tập train
"""

!gdown --id 1CsH5IVCOSVkLw8O77wBDfLOGpzk4zBzc
!unzip -qq archive.zip

"""DATASET PPM GGDRIVE"""

!gdown --id 1KRVUTDyiOm_W7WupL6pPGvgDHYBlPoDu
!unzip -qq train.zip

# List to store image data
data = []
# List to store image labels (classes)
labels = []
# Number of classes
classes = 43
# Current path of the dataset
current_path = '/content/'


# Iterates between 0 and 42 (43 classes)
for i in range(classes):
    
    # Path of each image
    path = os.path.join(current_path, 'train', str(i))
    images = os.listdir(path)
    
    # Iterates between each image
    for a in images:
        # Try to load the images
        try:
            # Open the image
            image = Image.open(path + '/' + a, mode='r')
            # Resizes the image to 30x30
            image = image.resize((30, 30))
            # Turns the image into an array
            image = np.array(image)
            # Append the image to "data" list
            data.append(image)
            # Append the label to "labels" list
            labels.append(i)
        # If it doesn't work, shows an error message
        except:
            print('DONE')

# Turns lists into array
data = np.array(data)
labels = np.array(labels)

print('DATA SHAPE: ', data.shape)
print('LABELS SHAPE', labels.shape)

# 20% to train
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.2, random_state=42)

print(X_train.shape,'|', X_test.shape,'|',y_train.shape,'|',y_test.shape)

# Use "to_categorical" method to convert the labels present in y_train and y_test into one-hot encoding
y_train = to_categorical(y_train, 43)
y_test = to_categorical(y_test, 43)

model = Sequential()

model.add(Conv2D(32, kernel_size=(5, 5), activation='relu', input_shape=X_train.shape[1:]))
model.add(Conv2D(32, kernel_size=(5, 5), activation='relu'))
model.add(MaxPool2D(2,2))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(2, 2))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dropout(0.5))

model.add(Dense(43, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 15 epochs
history = model.fit(X_train, y_train, batch_size=64, epochs=20, validation_data=(X_test, y_test))

# Figure size
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
# Plot train and validation accuracy
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='validation accuracy')
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()


plt.subplot(1, 2, 2)
# Plot loss and validation loss
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

y_test = pd.read_csv('/content/Test.csv')
y_test.head()

# Target
labels = y_test['ClassId'].values
# Test data path
current_path = '/content/'
# Images path
imgs = current_path + y_test['Path'].values

# Store image data
data = []


for img in imgs:
    # Open image
    image = Image.open(img)
    # Resize to 30x30
    image = image.resize((30, 30))
    # Append in "data" list
    data.append(np.array(image))
    
# Convert "data" list to array
X_test = np.array(data)

# Make predictions
preds = model.predict_classes(X_test)

# Evaluate model
print('ACCURACY: {} %'.format(round(accuracy_score(labels, preds) * 100, 3)))

model.save('traffic_classifier.h5')