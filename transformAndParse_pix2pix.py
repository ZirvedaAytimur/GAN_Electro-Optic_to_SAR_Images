import os
from fnmatch import fnmatch
from osgeo import gdal
import random
import shutil
import cv2
import numpy as np
import argparse


def parsing_data(path, data_type, images):
    path_for_data = os.path.join(path, data_type)
    os.mkdir(path_for_data)

    for image in images:
        source_path = os.path.join(path, image)
        shutil.move(source_path, path_for_data)


def selecting_images(i, path, percentage):
    data_number = int(i * percentage / 100)
    # find all filenames in folder
    filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # randomly select data
    images = random.sample(filenames, data_number)

    return images


def delete_xml_files(path):
    filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    pattern = "*xml*"

    for file in filenames:
        if fnmatch(file, pattern):
            os.remove(os.path.join(path, file))


def normalization_of_S1_data(root):
    for pathRoot, subdirs, files in os.walk(root):
        for name in files:
            path = pathRoot + '/' + name
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img2 = np.zeros_like(img)
            img2[:, :, 0] = gray
            img2[:, :, 1] = gray
            img2[:, :, 2] = gray
            cv2.imwrite(path, img2)


def find_and_transform_data_to_tif(sentinel_type, parent_directory, root, folder_names_percentages):
    # the data is represented by numbers so that the format is the same
    i = 0

    # create sentinel file
    path = os.path.join(parent_directory, sentinel_type + "_tif")
    os.mkdir(path)

    # search in the searching directory to find all types
    if sentinel_type == "A":
        pattern = "*s2*"
    else:
        pattern = "*s1*"
    for pathRoot, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                i += 1
                source = pathRoot + '/' + name

                # reassign band list with gdal
                ds = gdal.Open(source)
                file_name = parent_directory + '/' + sentinel_type + '_tif/' + str(i) + '.tif'
                if sentinel_type == "B":
                    ds = gdal.Translate(file_name, ds, bandList=[2, 2, 2], scaleParams=[[0, 3500]])
                elif sentinel_type == "A":
                    ds = gdal.Translate(file_name, ds, bandList=[4, 3, 2], scaleParams=[[0, 3500]])

                ds = None

    create_jpg_files(sentinel_type, parent_directory, folder_names_percentages)


def create_jpg_files(sentinel_type, parent_directory, folder_names_percentages):
    i = 0

    # create sentinel file
    path = os.path.join(parent_directory, sentinel_type)
    os.mkdir(path)

    for pathRoot, subdirs, files in os.walk(parent_directory + '/' + sentinel_type + '_tif'):
        for name in files:
            i += 1
            source = pathRoot + '/' + name

            # transform tif file to jpeg
            ds = gdal.Open(source)
            file_name = parent_directory + '/' + sentinel_type + '/' + str(i) + '.jpg'
            if sentinel_type == "B":
                options_list = [
                    '-ot Byte',
                    '-of JPEG',
                    '-b 1',
                    '-scale'
                ]

                options_string = " ".join(options_list)

            # sentinel type = A
            else:
                options_list = [
                    '-ot Byte',
                    '-of JPEG',
                    '-b 1',
                    '-b 2',
                    '-b 3'
                    '-scale'
                ]

                options_string = " ".join(options_list)

            ds = gdal.Translate(file_name, ds, options=options_string)
            ds = None

    delete_xml_files(path)

    if "test" in folder_names_percentages:
        test_images = selecting_images(i, path, folder_names_percentages["test"])
        parsing_data(path, "test", test_images)

    if "val" in folder_names_percentages:
        validation_images = selecting_images(i, path, folder_names_percentages["val"])
        parsing_data(path, "val", validation_images)

    if "train" in folder_names_percentages:
        train_images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        parsing_data(path, "train", train_images)

    if sentinel_type == "B":
        normalization_of_S1_data(parent_directory + '/' + sentinel_type)


if __name__ == '__main__':

    parser = argparse.ArgumentParser('transform image')
    parser.add_argument('--created_folder_director', dest='parent_directory', type=str)
    parser.add_argument('--searching_folder_directory', dest='root', type=str)
    args = parser.parse_args()

    # print("Parent directory path to create folders: ")
    # parent_directory = input()
    # print("Root of searching directory to be searched: ")
    # root = input()

    folder_names_percentages = {}
    folder_types = ["test", "val", "train"]
    for folder_type in folder_types:
        print("Shall create type ", folder_type, "?(1 for YES, 0 for NO)")
        answer = int(input())
        if answer == 1:
            print("Data percentage for folder: ")
            percentage = int(input())
            folder_names_percentages[folder_type] = percentage

    print("Number of image types: ")
    number_of_types = int(input())

    for i in range(number_of_types):
        print("Enter the ", i + 1, ". search pattern(s1 for Sentinel-1, s2 for Sentinel-2): ")
        sentinel_type = input()
        while sentinel_type not in ('s1', 's2'):
            print("Enter the ", i + 1, ". search pattern(s1 for Sentinel-1, s2 for Sentinel-2): ")
            sentinel_type = input()
        if sentinel_type == "s1":
            folder_type = "B"
        elif sentinel_type == "s2":
            folder_type = "A"
        random.seed(1)
        find_and_transform_data_to_tif(folder_type, args.parent_directory, args.root, folder_names_percentages)
        folder_name = folder_type + "_tif"
        shutil.rmtree(os.path.join(args.parent_directory, folder_name))
