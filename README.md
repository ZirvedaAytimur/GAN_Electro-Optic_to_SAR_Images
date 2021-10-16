# Image Translation

#### requirements.txt

All libraries used can be found in requirements.txt file.

## main.py

The main.py file is run to test a big picture over the trained models. Here you can test on pix2pix or CycleGAN. The
image is given as input and is first cropped to 256*256 size images. Afterwards, predictions are made from the
fragmented images either in the existing 'model_pix2pix.h5' and 'model_cycleGAN.h5' models or in the new model to be
given. These predicted images are combined back to create an image in fake Sentinel-1 format.

### Used train dataset for pretrained model

[2020 IEEE GRSS DATA FUSION CONTEST](https://ieee-dataport.org/competitions/2020-ieee-grss-data-fusion-contest) used to
train models.

### pix2pix

#### transformAndParse_pix2pix.py

This file takes Sentinel-1 and Sentinel-2 images from their folders and applies the necessary preprocessing steps for
each. It also divides the data into folders as train, test and validation according to the user's request. Corresponding
images in a pair must be the same size and have the same filename. Therefore, this was taken into account when saving
the pictures.

It works with the following command;

```
python transformAndParse_pix2pix.py --created_folder_director /path/to/create/Folder --searching_folder_directory /path/to/search/directory
```

#### combine_A_and_B.py

In the pix2pix algorithm, the images must be in pair. This file has been created to match the pictures in separate
places.

It works with the following command;

```
python combine_A_and_B.py --fold_A /path/to/data/A --fold_B /path/to/data/B --fold_AB /path/to/data
```

#### createNPZFile_pix2pix.py

In the pix2pix algorithm I created, the pictures are taken as a numpy array, so the pair data to be trained is converted
to a numpy array.

It works with the following command;

```
python createNPZFile_pix2pix.py --path /path/to/images --npz_file_root /path/to/save_numpy_array
```

#### pix2pix.py

The pix2pix algorithm is created in this file, and it shows the results with an image includes 3 images and creates a
model in every 10 epochs.

It works with the following command;

```
python pix2pix.py --dataset_name /path/to/created_numpy_array
```

### CycleGAN

#### transformAndParse_cycleGAN.py

This file takes Sentinel-1 and Sentinel-2 images from their folders and applies the necessary preprocessing steps for
each. It also divides the data into folders as train, test and validation according to the user's request.

It works with the following command;

```
python transformAndParse_cycleGAN.py --created_folder_director /path/to/create/Folder --searching_folder_directory /path/to/search/directory
```

#### createNPZFile_cycleGAN.py

In the CycleGAN algorithm I created, the pictures are taken as a numpy array like pix2pix.

It works with the following command;

```
python createNPZFile_cycleGAN.py --path_A /path/to/images/A --path_B /path/to/images/B --path_npz /path/to/save_numpy_array
```

#### cycleGAN.py

The CycleGAN algorithm is created in this file and it shows the results with 2 images (A to B and B to A) includes 5
images and creates a model in every 10 epochs.

It works with the following command;

```
python cycleGAN.py --dataset_name /path/to/created_numpy_array
```

## Test Results Folder

This folder includes both model_pix2pix.h5 and model_CycleGAN_s2_to_s1.h5 results of test image electro-optic.tif.
Original SAR image can be seen in original-SAR.tif file. In Copernicus electro-optic.tif file can be found in name
S2A_MSIL2A_20210425T105021_N0300_R051_T31UDQ_20210425T135357 and original-SAR.tif with
S1B_IW_GRDH_1SDV_20210312T174004_20210312T174029_025985_03198C_CAB5.SAFE.