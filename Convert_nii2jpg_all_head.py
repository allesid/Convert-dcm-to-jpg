# Convert  nii images to jpg images

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import use
from matplotlib import pyplot as plt
import SimpleITK as sitk
# import nibabel as nib
# from nibabel.viewers import OrthoSlicer3D
import os
import pandas as pd
# import numpy as np
import sys
use("TkCairo", force=True)


plt.style.use('_mpl-gallery')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Define function which extracts header information in a dictionary
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def header_info(My_image):
    header = {}
    for k in My_image.GetMetaDataKeys():
        header[k] = My_image.GetMetaData(k)
    return(header)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def showNii(img):
    for i in range(img.shape[0]):
        imgf = np.flipud(np.array(img[i, :, :]))
        if np.any(imgf):
            plt.figure(figsize=(5, 5))
            # im = img[i, :, :].clip(np.mean(
            #     img[i, :, :])-np.std(img[i, :, :]), np.mean(img[i, :, :])+np.std(img[i, :, :]))
            # img[i, :, :].clip(-1000, 400)
            imgf = imgf.clip(-400, 400)
            plt.imshow(imgf, cmap='gray')
            plt.grid(visible=None)
            plt.show()
            plt.pause(0.001)


def showNii2(img, imgs):
    for i in range(img.shape[0]):
        imgf = np.flipud(np.array(img[i, :, :]))
        imgfs = np.flipud(np.array(imgs[i, :, :]))
        if np.any(imgfs):
            plt.figure(figsize=(5, 5))
            imgf = imgf.clip(-400, 400)
            plt.imshow(imgf, cmap='gray')
            plt.grid(visible=None)
            plt.show()
            plt.pause(0.001)
            plt.imshow(imgfs, cmap='gray')
            plt.grid(visible=None)
            plt.show()
            plt.pause(0.001)


def showJPGpart(img):
    print("Loaded image")
    plt.figure(figsize=(5, 5))
    plt.imshow(img, cmap='gray')
    plt.grid(visible=None)
    plt.show()
    plt.pause(0.001)

    r = 5
    for i in range(r):
        part = 255/r
        vfun = np.vectorize(lambda x: x if (
            x < part*(i+1) and x >= part*i) else 0)
        imgf = vfun(img)
        # imgf = img.clip(25*i, 25*(i+1))
        plt.figure(figsize=(5, 5))
        plt.imshow(imgf, cmap='gray')
        plt.grid(visible=None)
        plt.show()
        plt.pause(0.001)


def showSeg(img):
    plt.figure(figsize=(5, 5))
    plt.imshow(img[0], cmap='gray')
    plt.grid(visible=None)
    plt.show()
    plt.pause(0.001)


def showNii1(img):
    im = img.shape[0]//2
    plt.figure(figsize=(5, 5))
    plt.imshow(img[im, :, :], cmap='gray_r')
    plt.grid(visible=None)
    plt.show()
    plt.pause(0.001)

    imgf = np.flipud(np.array(img[im, :, :])).clip(-300, 300)
    plt.figure(figsize=(5, 5))
    plt.imshow(imgf, cmap='gray')
    plt.grid(visible=None)
    plt.show()
    plt.pause(0.001)
    return imgf


def convert_nii2jpg(nii_folder_path="nii_imgs", jpg_folder_path="JPG_imgs",
                    img_info_fn="Images_information.csv"):
    """
    Read images in  .nii format and convert them into .jpg images.
    Also extract image information from .nii image into .csv file.

    Inputs:
    nii_folder_path:  Specify the folder path for .nii  images. Default: "nii_imgs".
    jpg_folder_path:  Specify the folder path for .jpg  images. Default: "JPG_imgs".
                        If jpg_folder_path is missing, create default folder.
    img_info_fn:         Specify name for image information file. Default: "Images_information.csv"

    Returns:
    None
    """
    if os.path.exists(nii_folder_path):
        images_path = os.listdir(nii_folder_path)
        print("images_path=", images_path)
    else:
        print(
            f"Folder path for .nii images is missing. Create {nii_folder_path} folder and copy .nii images into it")
        sys.exit(0)

    if not os.path.exists(jpg_folder_path):
        print(
            f"Folder path for .jpg  images is missing. Creating one: {jpg_folder_path}")
        os.mkdir(jpg_folder_path)

    # Conversion
    #Extract and save header data in numpy format
    for i in range(len(images_path)):
        itk_img = sitk.ReadImage(os.path.join(nii_folder_path, images_path[i]))
        img = sitk.GetArrayFromImage(itk_img)
        print(img.shape)
        print(np.unique(img))
        # fig, ax = plt.subplots()
        # ax.hist(np.unique(img), bins=30, linewidth=0.05, edgecolor="white")  # bins=8,
        # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        #     ylim=(0, 56), yticks=np.linspace(0, 56, 9))
        # plt.show()
        # plt.figure(figsize=(5, 5))
        # sns.histplot(data=np.ravel(img),
        #              bins=50, legend=False)
        # showSeg(img)
        showNii(img)
        # img = showNii1(img)
        # imagefn = images_path[i].replace('.nii', '')
        # plt.imsave(os.path.join(jpg_folder_path, imagefn+'.jpg'),
        #            img, cmap="gray")
        # img = imread(os.path.join(jpg_folder_path, imagefn+'.jpg'))
        # showJPGpart(img)
        header = header_info(itk_img)
        # print(header)
        df = pd.DataFrame([[x for x in header.values()]],
                          columns=[k for k in header.keys()])
        header_path = "./"
        df.to_csv(header_path+img_info_fn)
        # information about images saved in file Images_information.csv


def take_nii_files(nii_folder_path="nii_imgs", jpg_folder_path="JPG_imgs", conv_fun=convert_nii2jpg):
    """
    Takes all DICOM files recurcsively and convert to JPG files.

    Inputs:
    nii_folder_path:  Specify the folder path for .nii  images. Default: "nii_imgs".
    jpg_folder_path:  Specify the folder path for .jpg  images. Default: "JPG_imgs".
                        If jpg_folder_path is missing, create default folder.
    conv_fun:         Specify conversion function. Default: "convert_nii2jpg"

    Output:
    Files in jpg format

    Returns:
    None

    Directories structure in jpg_folder_path is the same as in nii_folder_path
    """
    if not os.path.exists(nii_folder_path):
        print(
            f"Folder path for .nii  images is missing. Create {nii_folder_path} folder and copy .nii  images into it")
        sys.exit(0)
# os.makedirs(name, mode=0o777, exist_ok=True)

    with os.scandir(nii_folder_path) as it:
        for entry in it:
            if entry.is_dir():
                nii_fpath = os.path.join(nii_folder_path, entry.name)
                jpg_fpath = os.path.join(jpg_folder_path, entry.name)
                os.makedirs(jpg_fpath, exist_ok=True)
                take_nii_files(nii_fpath, jpg_fpath, conv_fun)
            elif not entry.name.startswith('.') and entry.is_file():
                if entry.name.endswith('.nii'):  #
                    conv_fun(nii_folder_path, jpg_folder_path)
                    return
                else:
                    continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--niipath', default="nii_imgs",
                        help='Specify the folder path for .nii  images. Default: "nii_imgs".')
    parser.add_argument('-j', '--jpgpath', default="JPG_imgs",
                        help='Specify the folder path for .jpg  images. Default: "JPG_imgs".')
    parser.add_argument('-i', '--info', default="Images_information.csv",
                        help='Specify name for image information file. Default: "Images_information.csv"')
    args = parser.parse_args()
    nii_folder_path = args.niipath
    jpg_folder_path = args.jpgpath
    img_info_fn = args.info
    take_nii_files(nii_folder_path, jpg_folder_path, conv_fun=convert_nii2jpg)
    # convert_nii2jpg(nii_folder_path, jpg_folder_path, img_info_fn)
