import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras import models
from keras.layers import Flatten, Dense
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils.np_utils import to_categorical


df_train = pd.read_csv('../Preprocessing/solver_train_data.csv', index_col=False)
df_train = df_train.sample(frac=1)
labels = df_train.pop('784')
print(len(df_train))
print(df_train.head())

y_train = to_categorical(labels).astype('float32')
print(y_train[0])
x_train = df_train.to_numpy().reshape((-1, 28, 28, 1))
x_train = x_train.astype('float32')/255
print(x_train[0])

model = models.Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=x_train[0].shape))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(16, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=5, batch_size=64, shuffle=True, validation_split=0.1)

# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epochs')
# plt.legend(['train', 'val'])
# plt.show()

json_model = model.to_json()
with open("solver_model.json", "w") as json_file:
    json_file.write(json_model)
model.save_weights("solver_model_weights.h5")
