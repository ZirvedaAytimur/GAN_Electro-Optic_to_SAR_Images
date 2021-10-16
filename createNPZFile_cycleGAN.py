from os import listdir
from numpy import asarray, vstack, savez_compressed
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import argparse


def load_images(path, size=(256, 256)):
    data_list = list()
    for filename in listdir(path):
        pixels = load_img(path + filename, target_size=size)
        pixels = img_to_array(pixels)
        data_list.append(pixels)
    return asarray(data_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('create NPZ file')
    parser.add_argument('--path_A', dest='path_A', type=str)
    parser.add_argument('--path_B', dest='path_B', type=str)
    parser.add_argument('--path_npz', dest='path_npz', type=str)
    args = parser.parse_args()

    dataA1 = load_images(args.path_A + '/trainA/')
    dataAB = load_images(args.path_A + '/testA/')
    dataA = vstack((dataA1, dataAB))
    print('Loaded dataA: ', dataA.shape)

    dataB1 = load_images(args.path_B + '/trainB/')
    dataBA = load_images(args.path_B + '/testB/')
    dataB = vstack((dataB1, dataBA))
    print('Loaded dataB: ', dataB.shape)

    filename = 's2_to_s1.npz'
    savez_compressed(args.path_npz + '/' + filename, dataA, dataB)
    print('Saved dataset: ', filename)
