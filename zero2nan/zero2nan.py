#!/usr/bin/env python3
"""
Author : Michele Cosi
Date   : 2020-08-04
Purpose: Set all 0 values to NaN
"""

import argparse
import os
import sys
import subprocess
import glob
import numpy as np
from osgeo import gdal
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Corrects flir tifs that are are "white".',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('flirimg_in',
                        metavar='flir image to correct',
                        type=str,
                        help='Flir image that needs to be modified (0 vals to nan) in tif format.')

    parser.add_argument('-O',
                        '--outdir',
                        help='Path to Output directory',
                        metavar='Output directory',
                        type=str,
                        default='zero2nan_out')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='out tiffile name',
                        type=str,
                        help='name of the output tiffile (e.g., outfile.tif)',
                        default='outfile.tif')

    args = parser.parse_args()

    if '/' not in args.outdir:
        args.outdir = args.outdir + '/'

    if '.tif' not in args.outfile:
        args.outfile = args.outfile + '.tif'
    
    return args

# --------------------------------------------------
def main():
    
    # Load arguments
    args = get_args()

    # Read image from argument
    img_in = args.flirimg_in
    im = gdal.Open(img_in)
    raster = im.GetRasterBand(1)
    data = raster.ReadAsArray()
    
    data_array = np.array(data)
    data_array[data_array == 0] = np.nan

    driver = gdal.GetDriverByName('GTiff')
    dst_filename = (args.outfile)
    dst_ds = driver.CreateCopy( dst_filename, im, 0,[ 'TILED=YES', 'COMPRESS=PACKBITS' ] )

    dst_ds.GetRasterBand(1).WriteArray(data_array)
    dst_ds.FlushCache()

    print(f'done. Check {args.outfile} in this directory.')

    return dst_ds, dst_ds.GetRasterBand(1)
# --------------------------------------------------
if __name__ == '__main__':
    main()
