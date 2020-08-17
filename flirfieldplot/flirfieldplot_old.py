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

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create a stitched "ortho" for the flir imaegs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='input directory',
                        help='Input directory of plot directories')

    # parser.add_argument('-o',
    #                     '--outdir',
    #                     help='Output directory',
    #                     metavar='output directory',
    #                     type=str,
    #                     default='mean_temp_out')

    parser.add_argument('-d',
                        '--date',
                        help='processing date',
                        metavar='date of flir files you are processing',
                        type=str,
                        default='stitched')

    args = parser.parse_args()

    if '/' not in args.dir:
        args.dir = args.dir + '/'
    # if '/' not in args.outdir:
    #     args.outdir = args.outdir + '/'

    return args

# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    cmd = f'gdalbuildvrt mosaic.vrt {args.dir}*'
    subprocess.call(cmd, shell=True)
            
    cmd2 = f'gdal_translate -co COMPRESS=LZW -co BIGTIFF=YES -outsize 100% 100% mosaic.vrt {args.date}_ortho.tif'
    subprocess.call(cmd2, shell=True)

    print(f'Done. Find your output {args.date}_ortho.tif in this folder.')

# --------------------------------------------------
if __name__ == '__main__':
    main()
