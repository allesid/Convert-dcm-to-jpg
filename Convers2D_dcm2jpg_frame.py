# Convert 2D dcm images to jpg images

import pydicom as dicom
import os
import cv2
import pandas as pd
import numpy as np
import sys
from tqdm import tqdm


# def pix_coord(ipp, iop, ps, x, y):
    # a = iop[0] * ps[1]
    # b = ipp[0]
    # c = iop[3] * ps[0]
    # d = iop[1] * ps[1]
    # e = ipp[1]
    # f = iop[4] * ps[0]
    # px = int(((y-e)*c - f*(x-b))/(c*d-f*a))
    # py = int((y-e-d*px)/f)
    # return px, py

def pix_coord_s(ps, x, y):
    px = int(x/ps[1])
    py = int(512-y/ps[2])
    return px, py


# where x is the input value, y is an output value with a range from ymin to ymax, c is Window Center(0028, 1050) and w is Window Width(0028, 1051):
# def wconvs(x, wc, ww):
    # if (x <= (wc - 0.5 - (ww-1) / 2)):
        # y = 0
    # elif (x > (wc - 0.5 + (ww-1) / 2)):
        # y = 255
    # else:
        # y = ((x - (wc - 0.5)) / (ww-1) + 0.5) * 255
    # return y


def rectangle(img, t_start, t_end, colour):
    txstart = int(min(t_start[0], t_end[0]))
    txend = int(max(t_start[0], t_end[0]))
    tystart = int(min(t_start[1], t_end[1]))
    tyend = int(max(t_start[1], t_end[1]))
    for x in [txstart, txend]:
        for i in range(tystart, tyend+1):
            img[i,x] = colour
    for y in [tystart, tyend]:
        for i in range(txstart, txend+1):
            img[y, i] = colour
    return img

def convert2D_dcm2jpg(dcm_folder_path="DCM_imgs_2D", jpg_folder_path="JPG_imgs_2D",
                      img_info_fn="Images2D_information.csv"):
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
        # print("images_path=", images_path)
    else:
        print(
            f"Folder path for .dcm 2D images is missing. Create {dcm_folder_path} folder and copy .dcm 2D images into it")
        sys.exit(0)

    if not os.path.exists(jpg_folder_path):
        print(
            f"Folder path for .jpg 2D images is missing. Creating one: {jpg_folder_path}")
        os.mkdir(jpg_folder_path)

    # file "dicom_image_description.csv" consist of all available dicom image attributes
    dicom_image_description_file = "dicom_image_description_short.csv"
    annotation_file = "CrowdsCureCancer2017Annotations.csv"
    if os.path.exists(annotation_file):
        annots = pd.read_csv(annotation_file)
        print(annots)
    else:
        print(f"File {annotation_file} is absent.")
        sys.exit(0)
    if os.path.exists(dicom_image_description_file):
        params = pd.read_csv(dicom_image_description_file)
        print(params.columns)
        lp = len(params.columns)
        print('lp=', lp)
        pc = params.columns
    else:
        print(f"File {dicom_image_description_file} is absent.")
        sys.exit(0)

    # Conversion
    for image in images_path:
        # print("1\n",pc)
        if image.endswith(".dcm"):
            sopii = None
            print("===============================\n   image :", image)
            ds = dicom.dcmread(os.path.join(dcm_folder_path, image))
            img = ds.pixel_array
            print('img.shape=', img.shape)
            # img -= img[0, 0]
            if len(img.shape) != 2:
                print(
                    f"Input error: dcm file is {len(img.shape)} dimentional, expected 2 dimentions ")
                sys.exit(0)
            # print(params.columns)
            lp = len(pc)
            print('lp=', lp)
            # extract image information
            for field in pc:
                # print('field0=', field)
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

            if params.loc[lp, "SOPInstanceUID"] in list(annots["instanceUID"]):
                sopii = params.loc[lp, "SOPInstanceUID"]
                print('sopii=', sopii, ' type sopii=', type(sopii))
                ann = annots[annots["instanceUID"]
                             == sopii].reset_index()
                print(ann)
                xstart = ann.loc[0, "start_x"]
                ystart = ann.loc[0, "start_y"]
                xend = ann.loc[0, "end_x"]
                yend = ann.loc[0, "end_y"]
                print("xy=", xstart, ystart, xend, yend)
            if not sopii:
                print("IMAGE IS NOT IN ANNOTATION ")
                continue

            # print('field=', "ImagePositionPatient")
            s1 = params.loc[lp, "ImagePositionPatient"].removeprefix(
                "[").removesuffix("]").split(",")
            ipp = np.array(s1).astype(float)
            print('ipp=', ipp)
            # ipp = np.array([0,0,0])
            s1 = params.loc[lp, "ImageOrientationPatient"].removeprefix(
                "[").removesuffix("]").split(",")
            iop = np.array(s1).astype(float)
            print('iop=', iop)
            s1 = params.loc[lp, "PixelSpacing"].removeprefix(
                "[").removesuffix("]").split(",")
            ps = np.array(s1).astype(float)
            print('ps=', ps)
            # print(annots["instanceUID"])
            vfun = np.vectorize(lambda x: 250 if x>250 else x)
            img = vfun(img)
            img = (img / img.max()) * 255
            # vfun = np.vectorize(wconvs)
            # img = vfun(img, wc, ww)
            img = rectangle(img, (xstart, ystart),
                            (xend, yend), 255)
            # img = rectangle(img, (px_start, py_start),
                                # (px_end, py_end), 255)
            image = image.replace('.dcm', '')
            cv2.imwrite(os.path.join(jpg_folder_path,
                        image+'.jpg'), img)
        # print(f"{ds.filename} converted to jpg file")
        params = params.dropna(axis=1, how='all')
        # information about images saved in file Images2D_information.csv
        params.to_csv(img_info_fn)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dcmpath', default="DCM_imgs_2D",
                        help='Specify the folder path for .dcm 2D images. Default: "DCM_imgs_2D".')
    parser.add_argument('-j', '--jpgpath', default="JPG_imgs_2D",
                        help='Specify the folder path for .jpg 2D images. Default: "JPG_imgs_2D".')
    parser.add_argument('-i', '--info', default="Images2D_information.csv",
                        help='Specify name for image information file. Default: "Images2D_information.csv"')
    args = parser.parse_args()
    dcm_folder_path = args.dcmpath
    jpg_folder_path = args.jpgpath
    img_info_fn = args.info
    convert2D_dcm2jpg(dcm_folder_path, jpg_folder_path, img_info_fn)
