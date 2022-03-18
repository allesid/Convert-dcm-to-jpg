# Convert Nifti (nii) images to jpg images

import nibabel as nib
import os
import cv2
import sys
from tqdm import tqdm
import matplotlib.pyplot as plt

def convers_nii2jpg(nii_folder_path="nii_imgs", jpg_folder_path="JPG_imgs"): 
    """
    Read images in  .nii format and convert them into .jpg format.

    Inputs:
    nii_folder_path:  Specify the folder path for .nii  images. Default: "nii_imgs".
    jpg_folder_path:  Specify the folder path for .jpg  images. Default: "JPG_imgs".
                        If jpg_folder_path is missing, create default folder "JPG_imgs".

    Returns:
    None
    """
    
    if os.path.exists(nii_folder_path):
        images_path = os.listdir(nii_folder_path)
    else:
        print(
            f"Folder path for .nii  images is missing. Create {nii_folder_path} folder and copy .nii  images into it")
        sys.exit(0)

    if not os.path.exists(jpg_folder_path):
        print(
            f"Folder path for .jpg  images is missing. Creating one: {jpg_folder_path}")
        os.mkdir(jpg_folder_path)

    for n, image in enumerate(images_path):
        img_path = os.path.join(nii_folder_path, image)
        img = nib.load(img_path).get_fdata()
        image = image.replace('.nii.gz', '')

        for i in tqdm(range(img.shape[2])):
            img_2d = img[:, :, i]
            print(img_2d.shape)
            print(img_2d)
            sys.exit(0)
            cv2.imwrite(os.path.join(jpg_folder_path,
                        image+"_"+str(i)+'.jpg'), img_2d)
            plt.imshow(img_2d)  # отображаемое изображение
            plt.pause(0.001)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--niipath', default="nii_imgs",
                        help='Specify the folder path for .nii  images. Default: "nii_imgs".')
    parser.add_argument('-j', '--jpgpath', default="JPG_imgs",
                        help='Specify the folder path for .jpg  images. Default: "JPG_imgs".')
    args = parser.parse_args()
    nii_folder_path = args.niipath
    jpg_folder_path = args.jpgpath
    convers_nii2jpg(nii_folder_path, jpg_folder_path)
