#!/usr/bin/env python3
"""
Author : Michele Cosi
Date   : 2020-09-30
Purpose: Feature highlighting (not yet recogintion) for infrared images
"""

import argparse
import cv2
import sys
import csv
import os
import uuid
import glob
from osgeo import gdal
from terrautils.formats import create_geotiff

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='feature highlighting (not yet recogintion) for infrared images',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('tif',
                        metavar='geotiff',
                        help='TIFF file to be highlighted')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='str',
                        type=str,
                        default='clahe_out')

    args = parser.parse_args()

    if '/' not in args.outdir:
        args.outdir = args.outdir + '/'

    return args

# --------------------------------------------------

def main():
    """Highlight TIF here"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    tif_file = args.tif
    if tif_file is not None:
        out_file = os.path.join(args.outdir, tif_file.split('/')[-1])

        # Open file with GDAL
        # Get Projection 
        # Get Geo Transformation

        original_ds = gdal.Open(tif_file, 0) 
        sr = original_ds.GetProjection()   
        gt = original_ds.GetGeoTransform()

        # Get coordinates
        # Group into tuple in order of 
        # ( lat (y) min, lat (y) max, long (x) min, long (x) max)
        # Refer = https://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file
        # Terra = https://github.com/terraref/terrautils/blob/master/terrautils/formats.py

        width = original_ds.RasterXSize
        height = original_ds.RasterYSize
        minx = gt[0]
        miny = gt[3] + width*gt[4] + height*gt[5] 
        maxx = gt[0] + width*gt[1] + height*gt[2]
        maxy = gt[3] 
        gps_bounds = (miny, maxy, minx, maxx)

        # Open file with CV2
        # Normalize image

        img = cv2.imread(tif_file, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        normed = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        # Set Driver
        # Create empty GeoTIFF with original Y and X
####
        # drv = gdal.GetDriverByName("GTiff")
        # ds = drv.Create(out_file, img.shape[1], img.shape[0], 2, gdal.GDT_Float32)

        # # Set Geo Transform of new image as the same of the one from the old image
        # # Set Projection of new image as the same of the one from the old image

        # ds.SetGeoTransform(gt)
        # ds.SetProjection(sr)
        
        # # Carry out CLAHE (Contrast Limited Adaptive histogram equalization)
        # # Set CLAHE values as requried; grid size.

        clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10,10))
        cl1 = clahe.apply(normed)

        # ds.GetRasterBand(1).WriteArray(cl1)
        
        # # need to flush to data to visualize/save to file

        # ds = None
####                                
        #gps_bounds_bin, img_height, img_width = get_boundingbox(args.metadata, args.zoffset)
        
        # raw_data = np.fromfile(bin_file, np.dtype('<u2')).reshape(
        #     [480, 640]).astype('float')
        # raw_data = np.rot90(raw_data, 3)

        create_geotiff(cl1, gps_bounds, out_file, None,
                    True, None, None, compress=True)    
    
        print(f'CLAHE_for_{args.tif}_is_done.')

# --------------------------------------------------
if __name__ == '__main__':
    main()