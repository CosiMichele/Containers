#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez, Michele Cosi
Date   : 2020-06-21
Purpose: Calculate mean temperature for plots
References: TERRA-REF & AgPipeline
"""
import argparse
import cv2
import matplotlib.pyplot as plt
import matplotlib.pyplot
import numpy as np
CV_IO_MAX_IMAGE_PIXELS=None
import csv
import os
import uuid
from osgeo import gdal
import tifffile as tifi
import glob
from PIL import Image
import pandas as pd
import sys
import json


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='extract mean temperature from plots (.tif); returns a .csv file per plot',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='dir',
                        type=str,
                        help='Input plot directory')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='outdir',
                        type=str,
                        default='meantemp_out')

    parser.add_argument('-g',
                        '--geojson',
                        help='GeoJSON file with plot boundaries',
                        metavar='geojson',
                        type=str,
                        required=True)

    args = parser.parse_args()

    if '/' not in args.dir:
        args.dir = args.dir + '/'

    # if '/' not in args.outdir:
    #     args.outdir = args.outdir + '/'

    return args


# --------------------------------------------------
def get_trt_zones():
    trt_zone_1 = []
    trt_zone_2 = []
    trt_zone_3 = []

    for i in range(3, 19):
        for i2 in range(1, 48):
            plot = f'MAC_Field_Scanner_Season_10_Range_{i}_Column_{i2}'
            #print(plot)
            trt_zone_1.append(str(plot))

    for i in range(20, 36):
        for i2 in range(1, 48):
            plot = f'MAC_Field_Scanner_Season_10_Range_{i}_Column_{i2}'
            #print(plot)
            trt_zone_2.append(str(plot))

    for i in range(37, 53):
        for i2 in range(1, 48):
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

    return feat


# --------------------------------------------------
def main():
    args = get_args()
    
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)
    
    out_path = os.path.join(args.outdir, 'meantemp.csv')
    csv_file = open(out_path, 'a')
    csv_header = ','.join(['treatment','plot','genotype','longitude','latitude','mean_temp'])
    csv_file.write(csv_header + "\n")

    # Create list of tif images in directory
    img_list = glob.glob(f'{args.dir}/*/*.tif', recursive=True)
    let_dict = {}

    # Forloop: iterate list for each image
    img_n = 0
    
    for img in img_list:
        img_n += 1
        # Find name of each image
        img_name = os.path.basename(img)
        #date = '/'.join(os.path.splitext(os.path.basename(one_img.split('/')[-1]))[0].split('_')[1].split('.'))
        plot_raw = img.split('/')[-2]
        genotype = get_genotype(plot_raw, args.geojson)
        plot_name = '_'.join(plot_raw.split(' '))
        trt_zone = find_trt_zone(plot_name)

        # Load image with CV
        im = cv2.imread(img, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

        if im is not None:
            normed = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

            # Colour image gray
            im_color = cv2.applyColorMap(normed, cv2.COLORMAP_BONE)
            kernel = np.ones((1,1), np.uint8)

            #  Erode, dilate, and blur image for accurate contour detection
            img_erosion = cv2.erode(im_color, kernel, iterations=1)
            img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
            blur = cv2.GaussianBlur(img_dilation, (5,5), 1)           
            
            # Change colorspace and carry out edge detection for contour identification
            c_img = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
            kernel = np.ones((5,5), np.uint8)
            #edges = cv2.Canny(c_img,110,141)
            #res = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            
            # Find max peak (odd) and constant
            peaks = cv2.minMaxLoc(c_img)
            if (peaks[1] % 2) == 0:
                o_peaks = ((peaks[1]-1)/2)+((peaks[1]+1)/2)+1
            else:
                o_peaks = ((peaks[1]-1)/2)+((peaks[1]+1)/2)
            if peaks[1] >= 250:
                Const = 62

            if  250 > peaks[1] >= 240:
                Const = 42

            if 240 > peaks[1] >= 230:
                Const = 32
            #maxpeak = peaks[1]
            print(f'peaksloc: {peaks}\n') #minVal, maxVal, minLoc, maxLoc
            print(f'globalmax: {peaks[1]}\n')
            print(f'constant:{Const}\n')
            print(f'oddity:{o_peaks}\n')
            
            gaus = cv2.adaptiveThreshold(c_img, int(peaks[1]), cv2.ADAPTIVE_THRESH_MEAN_C, 
                                         cv2.THRESH_BINARY, int(o_peaks),int(Const))
            
            kernel = np.ones((30, 30), np.uint8)
            closing = cv2.morphologyEx(gaus, cv2.MORPH_OPEN, kernel)
            
            contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)           
            
            # Create mask and setup necessary variables for data collection
            canvas = im.copy()
            areas = {}
            num_cnt = 0
            shape = str(np.shape(canvas)).replace('(','').replace(')','')
            mask = np.zeros(im.shape, np.uint8)


            # Apply mask and extract name, meantemp, coords
            for c in contours:
                cnt = contours[0]
                M = cv2.moments(cnt)
                area = cv2.contourArea(c)

                if int(area) in range(10, 100000):
                    num_cnt += 1

                    # Create bounding box centered around contour
                    x,y,w,h = cv2.boundingRect(c)
                    cx = x+w//2
                    cy = y+h//2
                    center = (cx, cy)
                    dr = 30
                    cv2.rectangle(canvas, (int(cx-dr), int(cy-dr)), (int(cx+dr), int(cy+dr)), (0, 0, 255), 2)

                    # Draw the contours 
                    cv2.drawContours(im, contours, -1, (0,0,0), -1)

                    # Collect pixel coordinates and convert into lat, lon
                    pix_coord = str(center).strip('()')
                    x_pix, y_pix = pix_coord.split(',')
                    ds = gdal.Open(img)
                    c, a, b, f, d, e = ds.GetGeoTransform()
                    lon = a * int(x_pix) + b * int(y_pix) + a * 0.5 + b * 0.5 + c
                    lat = d * int(x_pix) + e * int(y_pix) + d * 0.5 + e * 0.5 + f
                    gps_coords = f'{lat}, {lon}'
                    
                    # Collect date and time (DATETIME)
                    
                    # Crop each contour for individual plant temp measurements 
                    cropped = im[cy-dr:cy+dr, cx-dr:cx+dr]
                    imarray = np.array(cropped)
                    imarray[imarray == 0] = np.nan
                    #stdev = np.std(cropped)
                    mean_tc = np.nanmean(imarray) - 273.15
                    print(img_name)
                    print(f'Temp: {mean_tc}\n')

                    csv_data = ','.join([str(trt_zone),
                                         str(plot_name),
                                         str(feat),
                                         str(lon),
                                         str(lat),
                                         str(mean_tc)])
                    csv_file.write(csv_data + "\n")
                    
                    # Print mask fig
                    
                    close_out_path = os.path.join(args.outdir,f'{img_n}.png')
                    cv2.imwrite(close_out_path, closing)
                                 
                    # Create dictionary with collected data
#                     let_dict[num_cnt] = {
#                         'treatment': trt_zone,
#                         'plot': plot_name,
#                         #'genotype': genotype,
#                         'longitude': lon,
#                         'latitude': lat,
#                         'mean_temp': mean_tc
#                     }
 
#     # Create dataframe and output a CSV from it
#     df = pd.DataFrame.from_dict(let_dict, orient='index', columns=['treatment', 
#                                                                     'plot', 
#                                                                     #'genotype', 
#                                                                     'longitude', 
#                                                                     'latitude', 
#                                                                     'mean_temp'])

#     if not os.path.isdir(args.outdir):
#         os.makedirs(args.outdir)

#     out_path = os.path.join(args.outdir, 'meantemp.csv')
#     df.to_csv(out_path, index=False)
    
    csv_file.close()
    print(f'Done. Find meantemp output in {out_path}')

# --------------------------------------------------
if __name__ == '__main__':
    main()
