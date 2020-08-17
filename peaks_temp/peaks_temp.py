#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez, Michele Cosi
Date   : 2020-07-02
Purpose: Mean temp extraction
"""

import argparse
import os
import sys
from osgeo import gdal
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from scipy import stats
from scipy.signal import find_peaks
import random
import statistics
import json

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='str',
                        help='A positional argument')

    parser.add_argument('-od',
                        '--outdir',
                        help='Output directory',
                        metavar='str',
                        type=str,
                        default='peak_mean_temp_out')

    parser.add_argument('-on',
                        '--outname',
                        help='Output filename',
                        metavar='str',
                        type=str,
                        default='peak_mean_temp')

    parser.add_argument('-g',
                        '--geo',
                        help='GeoJSON of plots',
                        type=str,
                        required=True)

    return parser.parse_args()


# --------------------------------------------------
def get_trt_zones():
    trt_zone_1 = []
    trt_zone_2 = []
    trt_zone_3 = []

    for i in range(3, 19):
        for i2 in range(2, 48):
            plot = f'MAC_Field_Scanner_Season_10_Range_{i}_Column_{i2}'
            #print(plot)
            trt_zone_1.append(str(plot))

    for i in range(20, 36):
        for i2 in range(2, 48):
            plot = f'MAC_Field_Scanner_Season_10_Range_{i}_Column_{i2}'
            #print(plot)
            trt_zone_2.append(str(plot))

    for i in range(37, 53):
        for i2 in range(2, 48):
            plot = f'MAC_Field_Scanner_Season_10_Range_{i}_Column_{i2}'
            #print(plot)
            trt_zone_3.append(str(plot))

    return trt_zone_1, trt_zone_2, trt_zone_3


# --------------------------------------------------
def find_trt_zone(plot_name):
    trt_zone_1, trt_zone_2, trt_zone_3 = get_trt_zones()
    #print(trt_zone_1)

    if plot_name in trt_zone_1:
        trt = 'treatment 1'

    elif plot_name in trt_zone_2:
        trt = 'treatment 2'

    elif plot_name in trt_zone_3:
        trt = 'treatment 3'

    else:
        trt = 'border'

    return trt


# --------------------------------------------------
def get_genotype(plot, geo):
    with open(geo) as f:
        data = json.load(f)

    for feat in data['features']:
        if feat.get('properties')['ID']==plot:
            genotype = feat.get('properties').get('genotype')

    return genotype


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    temp_dict = {}
    temp_cnt = 0
    img_list = glob.glob(f'{args.dir}/*/*.tif')
    print(img_list)

    # Forloop: iterate list for each image
    img_n = 0

    for one_img in img_list:
        
        img_n += 1
        
        temp_cnt += 1
        date = one_img.split('/')[-3][-10:]
        plot_raw = one_img.split('/')[-2]
        genotype = get_genotype(plot_raw, args.geo)
        plot_name = '_'.join(plot_raw.split(' '))
        trt_zone = find_trt_zone(plot_name)
        #print(f'{plot_name}')
        #print(f'{trt_zone}\n')
        print(f'Processing {plot_raw}')

        g_img = gdal.Open(one_img)
        a_img = g_img.GetRasterBand(1).ReadAsArray()
        m = stats.mode(a_img)
        mode, count = m
        peak = mode[0][0:5].mean()
        temp = peak - 273.15

        a_img[a_img > peak] = np.nan
        mean_tc = np.nanmean(a_img) - 273.15

        close_out_path = os.path.join(args.outdir,f'{img_n}.png')
        cv2.imwrite(close_out_path, g_img) 

        temp_dict[temp_cnt] = {
                'date': date,
                'treatment': trt_zone,
                'plot': plot_name,
                'genotype': genotype,
                'plot_temp': temp,
                'mean_plant_temp': mean_tc
                }
    df = pd.DataFrame.from_dict(temp_dict, orient='index', columns=['date',
                                                                    'treatment',
                                                                    'plot',
                                                                    'genotype',
                                                                    'plot_temp',
                                                                    'mean_plant_temp'])
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    df.to_csv(os.path.join(args.outdir, args.outname + '.csv'), index=False)   

    print(f'Done. Check outputs in {args.outdir}.')

# --------------------------------------------------
if __name__ == '__main__':
    main()
