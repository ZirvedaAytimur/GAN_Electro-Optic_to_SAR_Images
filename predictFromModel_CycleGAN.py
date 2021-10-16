from keras.models import load_model
from numpy import load
from numpy import vstack
from PIL import Image
import numpy as np


# load and prepare training images
def load_real_samples(filename):
    # load compressed arrays
    data = load(filename)
    # unpack arrays
    X1 = data['arr_0']
    # scale from [0,255] to [-1,1]
    X1 = (X1 - 127.5) / 127.5
    return [X1]


def normalize_image(image):
    v_min = image.min(axis=(1, 2, 3), keepdims=True)
    v_max = image.max(axis=(1, 2, 3), keepdims=True)
    normal_image = (image - v_min) / (v_max - v_min)

    return normal_image


def append_image(images, image_width, image_height, w, h, path):
    new_image = Image.new("RGB", (image_width, image_height), "white")

    frame_number = 0
    for col_i in range(0, image_width, w):
        for row_i in range(0, image_height, h):
            image = Image.fromarray((images[frame_number] * 255).astype(np.uint8))
            new_image.paste(image, (col_i, row_i))
            print('Appended: ', str(frame_number))
            frame_number += 1

    new_image.save(path + '/predicted.png')


def predict(path, model, image_width, image_height, predicted_path):
    # load dataset
    [X1] = load_real_samples(path)
    # load model
    model = load_model(model)
    src_image = X1[[0]]
    # generate image from source
    gen_image = model.predict(src_image)
    for i in range(1, len(X1)):
        src_image = X1[[i]]
        gen_image2 = model.predict(src_image)
        gen_image = vstack((gen_image, gen_image2))

    splited_number = 256
    normalized_image = normalize_image(gen_image)
    append_image(normalized_image, image_width, image_height, splited_number, splited_number, predicted_path)
