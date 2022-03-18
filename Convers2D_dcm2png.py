# Convert 2D dcm images to png images

import pydicom
import os
# import cv2
import pandas as pd
import numpy as np
import sys
from tqdm import tqdm
from PIL import Image
import matplotlib.pyplot as plt

def convert2D_dcm2png(dcm_folder_path="DCM_imgs_2D", png_folder_path="PNG_imgs_2D",
 img_info_fn="Images2D_information.csv"):

    """
    Read images in 2D .dcm format and convert them into .png images.
    Also extract image information from .dcm image into .csv file.
    File "dicom_image_description.csv" consist of all available dicom image attributes and must be present in scripts directory.

    Inputs:
    dcm_folder_path:  Specify the folder path for .dcm 2D images. Default: "DCM_imgs_2D".
    png_folder_path:  Specify the folder path for .png 2D images. Default: "PNG_imgs_2D".
                        If png_folder_path is missing, create default folder.
    img_info_fn:         Specify name for image information file. Default: "Images2D_information.csv"

    Returns:
    None
    """
    
    if os.path.exists(dcm_folder_path):
        images_path = os.listdir(dcm_folder_path)
    else:
        print(
            f"Folder path for .dcm 2D images is missing. Create {dcm_folder_path} folder and copy .dcm 2D images into it")
        sys.exit(0)

    if not os.path.exists(png_folder_path):
        print(
            f"Folder path for .png 2D images is missing. Creating one: {png_folder_path}")
        os.mkdir(png_folder_path)

    # file "dicom_image_description.csv" consist of all available dicom image attributes
    dicom_image_description_file = "dicom_image_description.csv"
    if os.path.exists(dcm_folder_path):
        params = pd.read_csv(dicom_image_description_file)
    else:
        print(f"File {dicom_image_description_file} is absent.")
        sys.exit(0)

    # Conversion
    for n, image in tqdm(enumerate(images_path)):
        if image.endswith(".dcm"):
            ds = pydicom.dcmread(os.path.join(
                dcm_folder_path, image), force=True)
            img = ds.pixel_array
            # print('pixel_array_numpy.shape=', pixel_array_numpy.shape)
            # img = (img - img.min()) / (img.max() - img.min()) * 255
            img_path = os.path.join(png_folder_path, image+"_"+str(n)+'.png')
            if ds.data_element("PhotometricInterpretation").value == "MONOCHROME1":
                plt.imsave(img_path, img, cmap="gray_r")
            elif ds.data_element("PhotometricInterpretation").value == "MONOCHROME2":
                plt.imsave(img_path, img, cmap="gray")

            if len(img.shape) != 2:
                print(
                    f"Input error: dcm file is {len(img.shape)} dimentional, expected 2 dimentions ")
                sys.exit(0)
            # cv2.imwrite(os.path.join(png_folder_path,
                        # image+"_"+str(n)+'.png'), img)
            lp = len(params)
            # extract image information
            for field in params.columns:
                try:
                    if ds.data_element(field) is None:
                        params.loc[lp, field] = None
                    else:
                        s1 = str(ds.data_element(field)).replace("'", "")
                        s2 = s1.find(":")
                        s1 = s1[s2+2:]
                        params.loc[lp, field] = s1
                except:
                    params.loc[lp, field] = None
        # print(f"{ds.filename} converted to png file")
        params = params.dropna(axis=1, how='all')
        # information about images saved in file Images2D_information.csv
        params.to_csv(img_info_fn)
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dcmpath', default="DCM_imgs_2D",
                        help='Specify the folder path for .dcm 2D images. Default: "DCM_imgs_2D".')
    parser.add_argument('-j', '--pngpath', default="PNG_imgs_2D",
                        help='Specify the folder path for .png 2D images. Default: "PNG_imgs_2D".')
    parser.add_argument('-i', '--info', default="Images2D_information.csv",
                        help='Specify name for image information file. Default: "Images2D_information.csv"')
    args = parser.parse_args()
    dcm_folder_path = args.dcmpath
    png_folder_path = args.pngpath
    img_info_fn = args.info
    convert2D_dcm2png(dcm_folder_path, png_folder_path, img_info_fn)
