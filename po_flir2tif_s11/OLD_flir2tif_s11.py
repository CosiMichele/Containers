#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez, Michele Cosi, Holly Ellingson, Jeffrey Demieville
Date   : 2020-07-09
Purpose: Convert FLIR .bin files to .tif
"""

import argparse
import os
import sys
import logging
import json
import numpy as np
import glob
from terrautils.spatial import scanalyzer_to_utm, geojson_to_tuples
from terrautils.formats import create_geotiff
import matplotlib.pyplot as plt
from osgeo import gdal, osr


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Season 11 flir2tif',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='str',
                        help='Directory containing bin and metadata files')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory where .tif files will be saved',
                        metavar='str',
                        type=str,
                        default='flir2tif_out')

    args = parser.parse_args()

    if '/' not in args.dir:
        args.dir = args.dir + '/'

    if '/' not in args.outdir:
        args.outdir = args.outdir + '/'

    return args



# --------------------------------------------------
def get_calibrate_param(metadata):
    calibparameter = calibParam()
    try:
        if 'terraref_cleaned_metadata' in metadata:
            fixedmd = metadata['sensor_fixed_metadata']
            # added this to pull in shutter temperature
            variablemd = metadata['sensor_variable_metadata']
            if fixedmd['is_calibrated'] == 'True':
                return calibparameter
            else:
                calibparameter.calibrated = False
                calibparameter.calibrationR = float(fixedmd['calibration_R'])
                calibparameter.calibrationB = float(fixedmd['calibration_B'])
                calibparameter.calibrationF = float(fixedmd['calibration_F'])
                calibparameter.calibrationJ1 = float(fixedmd['calibration_J1'])
                calibparameter.calibrationJ0 = float(fixedmd['calibration_J0'])
                calibparameter.calibrationa1 = float(
                    fixedmd['calibration_alpha1'])
                calibparameter.calibrationa2 = float(
                    fixedmd['calibration_alpha2'])
                calibparameter.calibrationX = float(fixedmd['calibration_X'])
                calibparameter.calibrationb1 = float(
                    fixedmd['calibration_beta1'])
                calibparameter.calibrationb2 = float(
                    fixedmd['calibration_beta2'])
                # To-Do: verify variable names to match what is present in cleaned metadata
                calibparameter.shuttertemperature = float(
                    variablemd['shutter_temperature_[K]'])
                return calibparameter
    except KeyError as err:
        return calibparameter


# --------------------------------------------------
def flirRawToTemperature(rawData, calibP):

    shutter_temp = calibP['content']['sensor_variable_metadata']['shutter_temperature_K']
    T = float(shutter_temp) - 273.15

    P_5_outmean = [1.137440642331793e-11,
                   -7.151963918140453e-07,
                   2.040023288027391e-02,
                   -1.480567234537099e+02]
    P_15_outmean = [1.081311914979629e-11,
                    -7.016010881023338e-07,
                    2.054630019627413e-02,
                    -1.521561215301546e+02]
    P_20_outmean = [7.884866004076222e-12,
                    -5.627752964123624e-07,
                    1.841833557270094e-02,
                    -1.424489740528044e+02]
    P_25_outmean = [9.583147873422692e-12,
                    -6.411047671547955e-07,
                    1.957403307722059e-02,
                    -1.488744387542483e+02]
    P_30_outmean = [7.731929583673130e-12,
                    -5.450000399690083e-07,
                    1.788280850465480e-02,
                    -1.397155089900219e+02]
    P_35_outmean = [9.979352154351443e-12,
                    -6.638673059086900e-07,
                    2.015587753410061e-02,
                    -1.556220395053390e+02]
    P_40_outmean = [1.113388420010232e-11,
                    -7.376131006851630e-07,
                    2.162806444290634e-02,
                    -1.657425341330783e+02]
    P_45_outmean = [8.689237696307418e-12,
                    -6.008401296566917e-07,
                    1.914217995514052e-02,
                    -1.514361986681356e+02]
    T_list = [5, 15, 20, 25, 30, 35, 40, 45]
    a = [P_5_outmean[0], P_15_outmean[0], P_20_outmean[0],
         P_25_outmean[0], P_30_outmean[0], P_35_outmean[0],
         P_40_outmean[0], P_45_outmean[0]]
    b = [P_5_outmean[1], P_15_outmean[1], P_20_outmean[1],
         P_25_outmean[1], P_30_outmean[1], P_35_outmean[1],
         P_40_outmean[1], P_45_outmean[1]]
    c = [P_5_outmean[2], P_15_outmean[2], P_20_outmean[2],
         P_25_outmean[2], P_30_outmean[2], P_35_outmean[2],
         P_40_outmean[2], P_45_outmean[2]]
    d = [P_5_outmean[3], P_15_outmean[3], P_20_outmean[3],
         P_25_outmean[3], P_30_outmean[3], P_35_outmean[3],
         P_40_outmean[3], P_45_outmean[3]]

    # use numpy linear interpolation function to generate calibration coefficients for actual sensor temperature
    P_val = [np.interp(T, T_list, a), np.interp(T, T_list, b),
                       np.interp(T, T_list, c), np.interp(T, T_list, d)]
    im = rawData
    pxl_temp = P_val[0]*im**3 + P_val[1]*im**2 + P_val[2]*im + P_val[3]
    pxl_temp = pxl_temp.astype(int)
   
    return pxl_temp


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    files_path = args.dir

    bin_files = glob.glob(f'{files_path}*/*.bin')

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    for bin_file in bin_files:
        meta_file_cleaned = bin_file.replace(
            '_ir.bin', '_metadata_cleaned.json')

        with open(meta_file_cleaned, 'r') as mdf:
            full_md = json.load(mdf)
            extractor_info = None

            if full_md:
                if bin_file is not None:
                    out_file = os.path.join(args.outdir, bin_file.split('/')[-1].replace(".bin", ".tif"))
                    gps_bounds_bin = geojson_to_tuples(
                        full_md['content']['spatial_metadata']['flirIrCamera']['bounding_box'])
                    raw_data = np.fromfile(bin_file, np.dtype('<u2')).reshape(
                        [480, 640]).astype('float')
                    raw_data = np.rot90(raw_data, 3)
                    tc = flirRawToTemperature(raw_data, full_md)
                    print(tc)

                    create_geotiff(tc, gps_bounds_bin, out_file, None,
                                False, extractor_info, None, compress=True)


# --------------------------------------------------
if __name__ == '__main__':
    main()
