import cv2
import numpy as np
import os


def show_image(img):
    cv2.imshow("preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def rotate_symbol(img, angle):
    _, img_binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    h, w = img.shape[:2]

    center = (w / 2, h / 2)

    rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    img_rotated = cv2.warpAffine(img_binary, rot_matrix, (w, h))

    img_final = cv2.bitwise_not(img_rotated)

    return img_final
    # show_image(img_final)


def expand_dataset(folder):
    images = os.listdir(folder)
    num_augmented = 6000 - len(images)
    print(num_augmented)
    i = 0

    for filename in images:
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)

        img_rotate_10 = rotate_symbol(img, 10)
        # img_flip_lr = cv2.flip(img, 1)
        img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)

        # print(folder + '/augmented_' + str(i) + '_flip_lr.jpg')
        # cv2.imwrite(folder + '/augmented_' + str(i) + '_flip_lr.jpg', img_flip_lr)
        cv2.imwrite(folder + '/augmented_' + str(i) + '_rotate_180.jpg', img_rotate_180)
        cv2.imwrite(folder + '/augmented_' + str(i) + '_rotate_10.jpg', img_rotate_10)
        i += 2

        if i > num_augmented+2:
            break


if __name__ == '__main__':
    expand_dataset("../Data/int")
