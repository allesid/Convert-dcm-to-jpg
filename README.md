# Conversion dcm to jpg images

Conversion DICOM images with dcm extension to jpg images and extracting images attributes according to DICOM standarts.

Converting and extracting 2D and 3D DICOM images.

DICOM images need to be copied to "DCM_imgs_2D/3D" directory, output jpg images extracting to "JPG_imgs_2D/3D" directory.

Images attributes saving to "Images2D_information.csv" or "Images3D_information.csv" files.

File "dicom_image_description.csv" contains all standard DICOM attributes.
It need for attributes extraction.

Usage:

python3 Convers2D_dcm2jpg.py [-d DCMDIRECTORY] [-j JPGDIRECTORY] [-i IMAGESINFOFILENAME]

where:

    DCMDIRECTORY:       Specify the folder path for .dcm 2D images. Default: "DCM_imgs_2D".
    JPGDIRECTORY:       Specify the folder path for .jpg 2D images. Default: "JPG_imgs_2D".
                        If jpg_folder_path is missing, default folder "JPG_imgs_2D" creates.
    IMAGESINFOFILENAME: Specify name for image information file. Default: "Images2D_information.csv"

The same usage with Convers3D_dcm2jpg.py module