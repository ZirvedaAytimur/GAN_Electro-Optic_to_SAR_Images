import numpy as np
import cv2
from PIL import Image


def crop_images(filename, w, h, image_width, image_height):
    img = cv2.imread(filename)
    # the image looked blue because it was in bgr format convert it to rgb format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_number = 1
    numpy_data = []
    for col_i in range(0, image_width, w):
        for row_i in range(0, image_height, h):
            crop = img[row_i:row_i + h, col_i:col_i + w]
            numpy_data.append(np.asarray(crop))
            print('Cropped: ', str(frame_number))
            frame_number += 1

    return numpy_data


def crop_test_path(path, numpyArray_test_path):
    image = Image.open(path)
    image_width, image_height = image.size

    # crop image
    numpy_data = crop_images(path, 256, 256, image_width, image_height)

    np.savez_compressed(numpyArray_test_path + '/' + 'cropped_image.npz', numpy_data)

    return numpyArray_test_path + '/' + 'cropped_image.npz'
