import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import random
import pandas as pd
import json
from datetime import datetime
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter.ttk import *
import subprocess
from pathlib import Path

###########
# GUI setup
root = Tk()
root.title('Environmental logger data parser')
root.geometry("850x280")

#########################
# Comboboxes and text box

## Season picker
season_combo= Combobox(root)
season_combo['values']=('season_10_yr_2020', 'season_11_yr_2020')
season_combo.get()

## Date picker
date_combo = Combobox(root)
# date_combo['values']= ('2020-06-12','2020-06-13','2020-06-14','2020-06-15','2020-06-16','2020-06-17','2020-06-18','2020-06-19','2020-06-20','2020-06-21','2020-06-22','2020-06-23','2020-06-24','2020-06-25','2020-06-26','2020-06-27','2020-06-28','2020-06-29','2020-06-30','2020-07-01','2020-07-02','2020-07-03','2020-07-05','2020-07-06','2020-07-10','2020-07-13','2020-07-19','2020-07-20','2020-07-23','2020-07-24','2020-07-25','2020-08-03','2020-08-08','2020-08-10','2020-08-15','2020-08-17','2020-08-18','2020-08-20','2020-08-21','2020-08-22','2020-08-24','2020-08-25','2020-08-30','2020-08-31','2020-09-07','2020-09-09','2020-09-14','2020-09-16','2020-09-19','2020-09-21','2020-09-23','2020-09-26','2020-09-28','2020-09-30','2020-10-03','2020-10-05','2020-10-07','2020-10-10','2020-10-12','2020-10-14','2020-10-17','2020-10-19','2020-10-21','2020-10-24','2020-10-26','2020-10-27','2020-10-28','2020-10-31','2020-11-02','2020-11-03','2020-11-04','2020-11-05','2020-11-06','2020-11-07','2020-11-08','2020-11-09','2020-11-10','2020-11-11','2020-11-12','2020-11-13')
# date_combo['values']=('2019-07-01','2019-07-05','2019-07-07','2019-07-08','2019-07-31','2019-08-01','2019-08-02','2019-08-03','2019-08-04','2019-08-05','2019-08-06','2019-08-07','2019-08-08','2019-08-09','2019-08-10','2019-08-11','2019-08-12','2019-08-13','2019-08-14','2019-08-15','2019-08-17','2019-08-18','2019-08-21','2019-08-22','2019-09-07','2019-09-08','2019-09-11','2019-09-12','2019-09-13','2019-09-16','2019-09-17','2019-09-18','2019-09-19','2019-09-23','2019-09-24','2019-09-25','2019-09-26','2019-09-27','2019-09-28','2019-10-02','2019-10-03','2019-10-04','2019-10-05','2019-10-06','2019-10-07','2019-10-08','2019-10-13','2019-10-14','2019-10-15','2019-10-16','2019-10-07','2019-10-08','2019-10-13','2019-10-14','2019-10-15','2019-10-16','2019-10-17','2019-10-18','2019-10-19','2019-10-20','2019-10-21','2019-10-27','2019-10-28','2019-10-29','2019-10-30','2019-10-31','2019-12-14','2019-12-16','2019-12-17','2019-12-18','2019-12-19','2019-12-20','2019-12-21','2019-12-22','2020-01-14','2020-02-16','2020-02-17','2020-02-23','2020-02-24','2020-02-25','2020-02-26','2020-02-27','2020-02-28','2020-02-29','2020-03-01','2020-03-02','2020-03-03','2020-03-10','2020-06-12','2020-06-13','2020-06-14','2020-06-15','2020-06-16','2020-06-17','2020-06-18','2020-06-19','2020-06-20','2020-06-21','2020-06-22','2020-06-23','2020-06-24','2020-06-25','2020-06-26','2020-06-27','2020-06-28','2020-06-29','2020-06-30','2020-07-01','2020-07-02','2020-07-03','2020-07-04','2020-07-05','2020-07-06','2020-07-07','2020-07-08','2020-07-09','2020-07-10','2020-07-11','2020-07-12','2020-07-13','2020-07-14','2020-07-15','2020-07-16','2020-07-17','2020-07-18','2020-07-19','2020-07-20','2020-07-21','2020-07-22','2020-07-23','2020-07-24','2020-07-25','2020-07-26','2020-07-27','2020-07-28','2020-07-29','2020-07-30','2020-07-31','2020-08-01','2020-08-02','2020-08-03','2020-08-04','2020-08-05','2020-08-06','2020-08-07','2020-08-08','2020-08-09','2020-08-10','2020-08-11','2020-08-12','2020-08-13','2020-08-14','2020-08-15','2020-08-16','2020-08-17','2020-08-18','2020-08-19','2020-08-20','2020-08-21','2020-08-22','2020-08-23','2020-08-24','2020-08-25','2020-08-26','2020-08-27','2020-08-28','2020-08-29','2020-08-30','2020-08-31','2020-09-01','2020-09-02','2020-09-03','2020-09-04','2020-09-05','2020-09-06','2020-09-07','2020-09-08','2020-09-09','2020-09-10','2020-09-11','2020-09-12','2020-09-13','2020-09-14','2020-09-15','2020-09-16','2020-09-17','2020-09-18','2020-09-19','2020-09-20','2020-09-21','2020-09-22','2020-09-23','2020-09-24','2020-09-25','2020-09-26','2020-09-27','2020-09-28','2020-09-29','2020-09-30','2020-10-01','2020-10-02','2020-10-03','2020-10-04','2020-10-05','2020-10-06','2020-10-07','2020-10-09','2020-10-10','2020-10-11','2020-10-12','2020-10-13','2020-10-14','2020-10-15','2020-10-16','2020-10-17','2020-10-19','2020-10-21','2020-10-22','2020-10-23','2020-10-24','2020-10-25','2020-10-26','2020-10-27','2020-10-28','2020-10-29','2020-10-30','2020-10-31','2020-11-02','2020-11-03','2020-11-04','2020-11-05','2020-11-06','2020-11-07','2020-11-08','2020-11-09','2020-11-10','2020-11-11','2020-11-12','2020-11-13')
date_combo['values']=('2019-07-01','2019-07-05','2019-07-07','2019-07-08','2019-07-31','2019-08-01','2019-08-02','2019-08-03','2019-08-04','2019-08-05','2019-08-06','2019-08-07','2019-08-08','2019-08-09','2019-08-10','2019-08-11','2019-08-12','2019-08-13','2019-08-14','2019-08-15','2019-08-17','2019-08-18','2019-08-21','2019-08-22','2019-09-07','2019-09-08','2019-09-11','2019-09-12','2019-09-13','2019-09-16','2019-09-17','2019-09-18','2019-09-19','2019-09-23','2019-09-24','2019-09-25','2019-09-26','2019-09-27','2019-09-28','2019-10-02','2019-10-03','2019-10-04','2019-10-05','2019-10-06','2019-10-07','2019-10-08','2019-10-13','2019-10-14','2019-10-15','2019-10-16','2019-10-07','2019-10-08','2019-10-13','2019-10-14','2019-10-15','2019-10-16','2019-10-17','2019-10-18','2019-10-19','2019-10-20','2019-10-21','2019-10-27','2019-10-28','2019-10-29','2019-10-30','2019-10-31','2019-11-01', '2019-11-02', '2019-11-03', '2019-11-04', '2019-11-05', '2019-11-06', '2019-11-07', '2019-11-08', '2019-11-09', '2019-11-10', '2019-11-11', '2019-11-12', '2019-11-13', '2019-11-14', '2019-11-15', '2019-11-16', '2019-11-17', '2019-11-18', '2019-11-19', '2019-11-20', '2019-11-21', '2019-11-22', '2019-11-23', '2019-11-24', '2019-11-25', '2019-11-26', '2019-11-27', '2019-11-28', '2019-11-29', '2019-11-30', '2019-12-01', '2019-12-02', '2019-12-03', '2019-12-04', '2019-12-05', '2019-12-06', '2019-12-07', '2019-12-08', '2019-12-09', '2019-12-10', '2019-12-11', '2019-12-12', '2019-12-13', '2019-12-14', '2019-12-15', '2019-12-16', '2019-12-17', '2019-12-18', '2019-12-19', '2019-12-20', '2019-12-21', '2019-12-22', '2019-12-23', '2019-12-24', '2019-12-25', '2019-12-26', '2019-12-27', '2019-12-28', '2019-12-29', '2019-12-30', '2019-12-31', '2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10', '2020-01-11', '2020-01-12', '2020-01-13', '2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21', '2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02', '2020-02-03', '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10', '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14', '2020-02-16', '2020-02-17', '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24', '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10','2020-06-12','2020-06-13','2020-06-14','2020-06-15','2020-06-16','2020-06-17','2020-06-18','2020-06-19','2020-06-20','2020-06-21','2020-06-22','2020-06-23','2020-06-24','2020-06-25','2020-06-26','2020-06-27','2020-06-28','2020-06-29','2020-06-30','2020-07-01','2020-07-02','2020-07-03','2020-07-04','2020-07-05','2020-07-06','2020-07-07','2020-07-08','2020-07-09','2020-07-10','2020-07-11','2020-07-12','2020-07-13','2020-07-14','2020-07-15','2020-07-16','2020-07-17','2020-07-18','2020-07-19','2020-07-20','2020-07-21','2020-07-22','2020-07-23','2020-07-24','2020-07-25','2020-07-26','2020-07-27','2020-07-28','2020-07-29','2020-07-30','2020-07-31','2020-08-01','2020-08-02','2020-08-03','2020-08-04','2020-08-05','2020-08-06','2020-08-07','2020-08-08','2020-08-09','2020-08-10','2020-08-11','2020-08-12','2020-08-13','2020-08-14','2020-08-15','2020-08-16','2020-08-17','2020-08-18','2020-08-19','2020-08-20','2020-08-21','2020-08-22','2020-08-23','2020-08-24','2020-08-25','2020-08-26','2020-08-27','2020-08-28','2020-08-29','2020-08-30','2020-08-31','2020-09-01','2020-09-02','2020-09-03','2020-09-04','2020-09-05','2020-09-06','2020-09-07','2020-09-08','2020-09-09','2020-09-10','2020-09-11','2020-09-12','2020-09-13','2020-09-14','2020-09-15','2020-09-16','2020-09-17','2020-09-18','2020-09-19','2020-09-20','2020-09-21','2020-09-22','2020-09-23','2020-09-24','2020-09-25','2020-09-26','2020-09-27','2020-09-28','2020-09-29','2020-09-30','2020-10-01','2020-10-02','2020-10-03','2020-10-04','2020-10-05','2020-10-06','2020-10-07','2020-10-09','2020-10-10','2020-10-11','2020-10-12','2020-10-13','2020-10-14','2020-10-15','2020-10-16','2020-10-17','2020-10-19','2020-10-21','2020-10-22','2020-10-23','2020-10-24','2020-10-25','2020-10-26','2020-10-27','2020-10-28','2020-10-29','2020-10-30','2020-10-31','2020-11-02','2020-11-03','2020-11-04','2020-11-05','2020-11-06','2020-11-07','2020-11-08','2020-11-09','2020-11-10','2020-11-11','2020-11-12','2020-11-13')
date_combo.get()

## Environmental variable picker
env_combo = Combobox(root)
env_combo['values']= ('Sun Direction','Air Pressure','Brightness','Precipitation','Relative humidity','Temperature','Wind direction','Wind velocity','Photosynthetically active radiation','Co2')
env_combo.get()

## Text box
T = tk.Text(root, height=15, width=72)
T.pack()
T.insert(tk.END, 'This is the Environmental parser for the gantry scanalyzer data. \nPlease select the season and day you are interested in viewing and \nselect "prep data"; \nThis will ensure data is downloaded and uncompressed. \nPlease give up to 10 minutes to donwload and uncompress your data, \ndepending on your internet connection. \nWhen data is ready, press "load data", please wait up to 1-2minutes. \nOnce loaded choose "day median" to view median of all collected \nenvironmental variables. \nIf you are interested in a specific data at a specific time, \nselect which environmental variable you are interested in and press \n"show graph". \nPlease keep in mind that the data might take a moment to load. \nThank you for using the Environmental parser.')

#################
# Unit dictionary
d_units = {                
    'Sun Direction' : "Sun Direction (degrees)",
    'Air Pressure': "Air Pressure (hPa)",
    'Brightness': "Brightness (kilo Lux)",
    'Precipitation': "Precipitation (mm/h)",
    'Relative humidity': "Relative humidity (relHum%)",
    'Temperature': "Temperature (C)",
    'Wind direction': "Wind direction (degrees)",
    'Wind velocity': "Wind velocity (m/s)",
    'Photosynthetically active radiation': "Photosynthetically active radiation (umol/(m^2*s))",
    'Co2': " Co2 (ppm)"}


################
# load data

def prep_data():

    # Download data

    Path.cwd()
    season = season_combo.get()
    date = date_combo.get()

    date_tar = Path(f'{date}_clean.tar.gz')
    uncompressed_tar = Path(f'{date}_clean.csv/')

    if uncompressed_tar.is_file():
        print("uncompressed exists, data loaded.")
        T.delete('1.0', END)
        T.insert(END, f'uncompressed exists, {date} data loaded.')
    else:
        if date_tar.is_file():
            T.delete('1.0', END)
            T.insert(END, f'tar exists, will uncompress and prep {date} data. Press prep data to test if loaded.')
            print("tar exists, will uncompress.")
            T.delete('1.0', END)
            T.insert(END, f'{date} data loaded.')
            # Untar data
            command = f'tar -xvf {date}_clean.tar.gz'
            subprocess.call(command, shell = True)
        else:
            T.delete('1.0', END)
            T.insert(END, f'tar does not exist, will download, uncompress and prep {date} data. Press prep data again to test if loaded.')
            print("tar does not exist, will download and uncompress.")
            command = f'iget -rKTPf -N 0 /iplant/home/shared/terraref/ua-mac/level_1/{season}/EnvironmentLogger/{date}_clean.tar.gz'
            subprocess.call(command, shell = True)
            command = f'tar -xvf {date}_clean.tar.gz'
            subprocess.call(command, shell = True)
            T.delete('1.0', END)
            T.insert(END, f'{date} data ready.')


def load_data():
        # time_start = "10:00" # Uncomment if want time beween timeframe
    # time_end = "23:00" # Uncomment if want time between timeframe

    global timeframe

    date = date_combo.get()
    
    d_all = pd.read_csv(f'./{date}_clean.csv')

    ## Format to datetime, sort, index
    d_all['Time'] = pd.to_datetime(d_all.Time)
    d_all = d_all.sort_values(by='Time')
    d_all = d_all.set_index('Time')

    ## Create subset according to time beginning and time end
    subset = d_all.resample("T").max() # per minute
    # subset = d_all.resample("60T").max() # per hour
    # timeframe = subset.between_time(time_start, time_end) # Uncomment if want to use timeframe
    timeframe = subset

    ## Set as float (required for graphing)
    timeframe['Sun Direction'] = timeframe['Sun Direction'].astype(float)
    timeframe['Air Pressure'] = timeframe['Air Pressure'].astype(float)
    timeframe['Brightness'] = timeframe['Brightness'].astype(float)
    timeframe['Precipitation'] = timeframe['Precipitation'].astype(float)
    timeframe['Relative humidity'] = timeframe['Relative humidity'].astype(float)
    timeframe['Temperature'] = timeframe['Temperature'].astype(float)
    timeframe['Wind direction'] = timeframe['Wind direction'].astype(float)
    timeframe['Wind velocity'] = timeframe['Wind velocity'].astype(float)
    timeframe['Photosynthetically active radiation'] = timeframe['Photosynthetically active radiation'].astype(float)
    timeframe['Co2'] = timeframe['Co2'].astype(float)

    T.delete('1.0', END)
    T.insert(END, f'{date} data loaded.')

    return timeframe

########
# Graph

def graph():

    date = date_combo.get()

    ## Create graph
    ### Format 
    print("Making graph... taking a while...")
    fig, ax = plt.subplots(1,1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) # ax = axis
    plt.ylabel(d_units[env_combo.get()])
    plt.xlabel('Time')

    ### Graph selected environmental factor
    plt.plot(timeframe[env_combo.get()]) # to be changed
    plt.show()

    print("Done")


def Daydata():

    date = date_combo.get()

    T.delete('1.0', END)
    T.insert(END,f'Medians for {date_combo.get()}: \nSun Direction: {timeframe["Sun Direction"].median()} degrees. \nAir Pressure: {timeframe["Air Pressure"].median()} hPa.\nBrightness: {timeframe["Brightness"].median()} kilo Lux.\nPrecipitation: {timeframe["Precipitation"].median()} mm/h.\nRelative humidity: {timeframe["Relative humidity"].median()} relHum%.\nTemperature: {timeframe["Temperature"].median()} C.\nWind direction: {timeframe["Wind direction"].median()} degrees.\nWind velocity: {timeframe["Wind velocity"].median()} m/s.\nPhotosynthetically active radiation:{timeframe["Photosynthetically active radiation"].median()} umol/(m^2*s).\nCo2: {timeframe["Co2"].median()} ppm.')

def Instr():
    T.delete('1.0', END)
    T.insert(tk.END, 'This is the Environmental parser for the gantry scanalyzer data. \nPlease select the season and day you are interested in viewing and \nselect "prep data"; \nThis will ensure data is downloaded and uncompressed. \nPlease give up to 10 minutes to donwload and uncompress your data, \ndepending on your internet connection. \nWhen data is ready, press "load data", please wait up to 1-2minutes. \nOnce loaded choose "day median" to view median of all collected \nenvironmental variables. \nIf you are interested in a specific data at a specific time, \nselect which environmental variable you are interested in and press \n"show graph". \nPlease keep in mind that the data might take a moment to load. \nThank you for using the Environmental parser.')

####################
# Buttons, placement

load_btn = Button(root, text = "load data", command = load_data)
load_btn.pack()

season_lbl = Label(root, text  = "Choose a season (required*)")
season_lbl.pack()

prep_button = Button(root, text = "prep data", command = prep_data)
prep_button.pack()

Graph_button = Button(root, text= "show graph", command = graph)
Graph_button.pack()

text_btn = Button(root, text= "day median", command = Daydata)
text_btn.pack()

Instr_btn = Button(root, text = "Instructions", command = Instr)
Instr_btn.pack

date_lbl = Label(root, text = "Choose a date (required*)")
date_lbl.pack()

env_lbl = Label(root, text = "Choose an environmental variable \n           (required to graph*)")
env_lbl.pack()

Instr_btn.place(x=90, y=10) # instruction button

season_lbl.place(x=42, y= 45) # season label
season_combo.place(x=45, y=65) # season combobox
date_lbl.place(x=47, y= 100) # date label
date_combo.place(x=45, y=120) # date combobox
prep_button.place(x= 5, y=150) # prep data button
load_btn.place(x=90, y=150) # load data button
text_btn.place(x=175, y= 150) # day data text button 
env_lbl.place(x=20, y= 180) # env label
env_combo.place(x=45, y= 220) # env combobox
Graph_button.place(x=90, y= 245) # graph button
T.place(x=267, y=10) # Text box

root.mainloop()