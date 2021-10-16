from os import listdir
from numpy import asarray
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from numpy import savez_compressed
import argparse


# load all images in a directory into memory
def load_images(path, size=(256, 512)):
    src_list, tar_list = list(), list()
    # enumerate filenames in directory, assume all are images
    for filename in listdir(path):
        # load and resize the image
        pixels = load_img(path + filename, target_size=size)
        # convert to numpy array
        pixels = img_to_array(pixels)
        # split into satellite and map
        source_image, expected_img = pixels[:, :256], pixels[:, 256:]
        src_list.append(source_image)
        tar_list.append(expected_img)
    return [asarray(src_list), asarray(tar_list)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser('create NPZ file')
    parser.add_argument('--path', dest='path', type=str)
    parser.add_argument('--npz_file_root', dest='root', type=str)
    args = parser.parse_args()
    # load dataset
    [src_images, tar_images] = load_images(args.path + '/')
    print('Loaded: ', src_images.shape, tar_images.shape)
    # save as compressed numpy array
    filename = 'data.npz'
    savez_compressed(args.root + '/' + filename, src_images, tar_images)
    print('Saved dataset: ', filename)
