# Convert 2D dcm images to jpg images

import pydicom as dicom
import os
import cv2
import numpy as np
import pandas as pd
import sys
from tqdm import tqdm



def convert2D_dcm2jpg(dcm_folder_path="DCM_imgs_2D", jpg_folder_path="JPG_imgs_2D",
 img_info_fn="Images2D_information.csv", brightp=1):

    """
    Read images in 2D .dcm format and convert them into .jpg images.
    Also extract image information from .dcm image into .csv file.
    File "dicom_image_description.csv" consist of all available dicom image attributes and must be present in scripts directory.

    Inputs:
    dcm_folder_path:  Specify the folder path for .dcm 2D images. Default: "DCM_imgs_2D".
    jpg_folder_path:  Specify the folder path for .jpg 2D images. Default: "JPG_imgs_2D".
                        If jpg_folder_path is missing, create default folder.
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

    if not os.path.exists(jpg_folder_path):
        print(
            f"Folder path for .jpg 2D images is missing. Creating one: {jpg_folder_path}")
        os.mkdir(jpg_folder_path)

    # file "dicom_image_description.csv" consist of all available dicom image attributes
    dicom_image_description_file = "dicom_image_description.csv"
    if os.path.exists(dicom_image_description_file):
        params = pd.read_csv(dicom_image_description_file)
    else:
        print(f"File {dicom_image_description_file} is absent.")
        sys.exit(0)

    # Conversion
    for n, image in tqdm(enumerate(images_path)):
        if image.endswith(".dcm"):
            ds = dicom.dcmread(os.path.join(dcm_folder_path, image))
            # print(ds.top())
            # print(ds.values())
            img = ds.pixel_array
            # print('pixel_array_numpy.shape=', pixel_array_numpy.shape)
            # img = (img - img.min()) / (img.max() - img.min()) * 255
            if n == 1:
                # print('img=\n', img)
                print('img.max=', img.max(), 'img.min=',
                      img.min(), 'img[0,0]=', img[0, 0])
            img = np.where(img > (img.max()//brightp), img.max()//brightp, img)
            img = (img - img.min()) / (img.max() - img.min()) * 255
            if len(img.shape) != 2:
                print(
                    f"Input error: dcm file is {len(img.shape)} dimentional, expected 2 dimentions ")
                sys.exit(0)
            image = image.replace('.dcm', '')
            cv2.imwrite(os.path.join(jpg_folder_path,
                        image+"_"+str(n)+'.jpg'), img)
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
        # print(f"{ds.filename} converted to jpg file")
        params = params.dropna(axis=1, how='all')
        # information about images saved in file Images2D_information.csv
        params.to_csv(img_info_fn)
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dcmpath', default="DCM_imgs_2D",
                        help='Specify the folder path for .dcm 2D images. Default: "DCM_imgs_2D".')
    parser.add_argument('-j', '--jpgpath', default="JPG_imgs_2D",
                        help='Specify the folder path for .jpg 2D images. Default: "JPG_imgs_2D".')
    parser.add_argument('-i', '--info', default="Images2D_information.csv",
                        help='Specify name for image information file. Default: "Images2D_information.csv"')
    parser.add_argument('-b', '--bright', default=1,
                        help='Specify below part of pixels values. Values range >=1 . Default: 1')
    args = parser.parse_args()
    dcm_folder_path = args.dcmpath
    jpg_folder_path = args.jpgpath
    img_info_fn = args.info
    brightp = int(args.bright)
    convert2D_dcm2jpg(dcm_folder_path, jpg_folder_path, img_info_fn, brightp)
