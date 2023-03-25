from keras.datasets import mnist
import cv2
import numpy as np
import pandas as pd
import os


def show_image(img):
    cv2.imshow("preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def load_symbol_dataset(folder):
    data = list()
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
        img = ~img
        if img is not None:
            _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            # show_image(thresh)

            img_resize = cv2.resize(thresh, (28, 28))
            # show_image(img_resize)

            _, img_resize_thresh = cv2.threshold(img_resize, 30, 255, cv2.THRESH_BINARY)
            # show_image(img_resize_thresh)
            #
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            # img_dilated = cv2.dilate(img_resize_thresh, kernel, iterations=1)
            # show_image(img_dilated)

            img_resize_thresh = np.reshape(img_resize_thresh, (784, ))

            data.append(img_resize_thresh)
    return data

# '+' - 10
data_plus = load_symbol_dataset('../Data/+')
data_plus = np.insert(data_plus, 784, 10, axis=1)
print(data_plus.shape)

# '-' - 11
data_minus = load_symbol_dataset('../Data/-')
data_minus = np.insert(data_minus, 784, 11, axis=1)
print(data_minus.shape)

# '*' - 12
data_times = load_symbol_dataset('../Data/times')
data_times = np.insert(data_times, 784, 12, axis=1)
print(data_times.shape)

# '=' - 13
data_equal = load_symbol_dataset('../Data/=')
data_equal = np.insert(data_equal, 784, 13, axis=1)
print(data_equal.shape)

# 'x' = 14
data_x = load_symbol_dataset('../Data/X')
data_x = np.insert(data_x, 784, 14, axis=1)
print(data_x.shape)

# 'y' = 15
data_y = load_symbol_dataset('../Data/Y')
data_y = np.insert(data_y, 784, 15, axis=1)
print(data_y.shape)

train_data = np.concatenate((data_plus, data_minus, data_times, data_equal, data_x, data_y))

for num in range(10):
    data_num = load_symbol_dataset(f'../Data/{num}')
    data_num = np.insert(data_num, 784, num, axis=1)
    train_data = np.concatenate((train_data, data_num))

df = pd.DataFrame(train_data, index=None)
df.to_csv('solver_train_data.csv', index=False)
