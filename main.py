from PIL import Image
import cropImages
import predictFromModel_CycleGAN
import predictFromModel_pix2pix

if __name__ == '__main__':
    print('Type 1 for pix2pix, 2 for CycleGAN.')
    choose_algorithm = int(input())
    while choose_algorithm not in (1, 2):
        print('Type 1 for pix2pix, 2 for CycleGAN.')
        choose_algorithm = int(input())

    print('Enter the image path.')
    path = input()
    print('Enter the path to save numpy array.')
    numpyArray_test_path = input()
    test_array = cropImages.crop_test_path(path, numpyArray_test_path)

    image = Image.open(path)
    image_width, image_height = image.size
    # pix2pix
    if choose_algorithm == 1:
        print('Do you want to use pretrained model? (yes or no)')
        pretrained_choice = input()
        while pretrained_choice not in ('yes', 'no'):
            print('Do you want to use pretrained model? (yes or no)')
            pretrained_choice = input()

        if pretrained_choice == 'yes':
            model = 'model_pix2pix.h5'
        else:
            print('Enter the model path.')
            model = input()

        print('Enter the path to save the predicted image.')
        predicted_path = input()

        predictFromModel_pix2pix.predict(test_array, model, image_width, image_height, predicted_path)

    # CycleGAN
    else:
        print('Do you want to use pretrained model? (yes or no)')
        pretrained_choice = input()
        while pretrained_choice not in ('yes', 'no'):
            print('Do you want to use pretrained model? (yes or no)')
            pretrained_choice = input()

        if pretrained_choice == 'yes':
            model = 'model_CycleGAN_s2_to_s1.h5'
        else:
            print('Enter the model path.')
            model = input()

        print('Enter the path to save the predicted image.')
        predicted_path = input()

        predictFromModel_CycleGAN.predict(test_array, model, image_width, image_height, predicted_path)
