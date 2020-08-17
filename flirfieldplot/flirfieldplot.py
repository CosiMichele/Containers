#!/usr/bin/env python3
"""
Author : Michele Cosi
Date   : 2020-08-07
Purpose: Create a stitched "ortho" for the flir imaegs
"""

import argparse
import cv2
import sys
import os
import uuid
from osgeo import gdal
import glob
import subprocess
from PIL import Image
import numpy as np

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create a stitched "ortho" for the flir imaegs. STRICTLY USE WITH SINGULARITY.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='input directory',
                        help='Input directory of plot directories')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='output directory',
                        type=str,
                        default='stitchedortho_out')

    parser.add_argument('-d',
                        '--date',
                        help='processing date',
                        metavar='date of flir files you are processing',
                        type=str,
                        default='stitched')

    args = parser.parse_args()

    if '/' not in args.dir:
        args.dir = args.dir + '/'
    if '/' not in args.outdir:
        args.outdir = args.outdir + '/'

    return args

# --------------------------------------------------
def stitch_ortho():
    """PART 1: stitch images into a full field plot"""

    args = get_args()

    cmd = f'gdalbuildvrt {args.outdir}mosaic.vrt {args.dir}*'
    subprocess.call(cmd, shell=True)
            
    cmd2 = f'gdal_translate -co COMPRESS=LZW -co BIGTIFF=YES -outsize 100% 100% {args.outdir}mosaic.vrt {args.outdir}{args.date}_ortho.tif'
    subprocess.call(cmd2, shell=True)

    return stitch_ortho

# --------------------------------------------------
def zero2nan():
    """PART 2: Convert pixel values == 0 to pixel values == NaN"""

    args = get_args()

    img_in = (f'{args.outdir}{args.date}_ortho.tif')
    print(img_in)
    im = gdal.Open(img_in)
    raster = im.GetRasterBand(1)
    data = raster.ReadAsArray()
    
    data_array = np.array(data)
    data_array[data_array == 0] = np.nan

    driver = gdal.GetDriverByName('GTiff')
    dst_filename = (f'{args.outdir}{args.date}_ortho_NaN.tif')
    dst_ds = driver.CreateCopy( dst_filename, im, 0,[ 'TILED=YES', 'COMPRESS=PACKBITS' ] )

    dst_ds.GetRasterBand(1).WriteArray(data_array)
    dst_ds.FlushCache()

    return zero2nan

# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    try:
        os.makedirs(args.outdir)
        print(f'Directory {args.outdir} created.')
    except FileExistsError:
        print(f'Directory {args.outdir} already exists.')

    # PART 1: stitch images into a full field plot
    stitch_ortho()

    # PART 2: Convert pixel values = 0 to pixel values = NaN
    zero2nan()

    print(f'Done. Find your outputs in {args.outdir} in this folder.')

# --------------------------------------------------
if __name__ == '__main__':
    main()