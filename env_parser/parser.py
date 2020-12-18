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
root.geometry("850x220")

#########################
# Comboboxes and text box

## Date picker
date_combo = Combobox(root)
date_combo['values']= ('2020-06-12','2020-06-13','2020-06-14','2020-06-15','2020-06-16','2020-06-17','2020-06-18','2020-06-19','2020-06-20','2020-06-21','2020-06-22','2020-06-23','2020-06-24','2020-06-25','2020-06-26','2020-06-27','2020-06-28','2020-06-29','2020-06-30','2020-07-01','2020-07-02','2020-07-03','2020-07-05','2020-07-06','2020-07-10','2020-07-13','2020-07-19','2020-07-20','2020-07-23','2020-07-24','2020-07-25','2020-08-03','2020-08-08','2020-08-10','2020-08-15','2020-08-17','2020-08-18','2020-08-20','2020-08-21','2020-08-22','2020-08-24','2020-08-25','2020-08-30','2020-08-31','2020-09-07','2020-09-09','2020-09-14','2020-09-16','2020-09-19','2020-09-21','2020-09-23','2020-09-26','2020-09-28','2020-09-30','2020-10-03','2020-10-05','2020-10-07','2020-10-10','2020-10-12','2020-10-14','2020-10-17','2020-10-19','2020-10-21','2020-10-24','2020-10-26','2020-10-27','2020-10-28','2020-10-31','2020-11-02','2020-11-03','2020-11-04','2020-11-05','2020-11-06','2020-11-07','2020-11-08','2020-11-09','2020-11-10','2020-11-11','2020-11-12','2020-11-13')
date_combo.get()

## Environmental variable picker
env_combo = Combobox(root)
env_combo['values']= ('Sun Direction','Air Pressure','Brightness','Precipitation','Relative humidity','Temperature','Wind direction','Wind velocity','Photosynthetically active radiation','Co2')
env_combo.get()

## Text box
T = tk.Text(root, height=12, width=72)
T.pack()
T.insert(tk.END, 'This is the Environmental parser for the gantry scanalyzer data. \nPlease select the day you are interested in viewing and select \n"prep data"; This will ensure data is downloaded and uncompressed - \nPlease give up to 10 minutes to donwload and uncompress your data, \ndepending on your internet connection. \nWhen data is ready, press "load data", please wait up to 1-2minutes. \nOnce loaded choose "day median" to view median of all collected \nenvironmental variables. \nIf you are interested in a specific data at a specific time, \nselect which environmental variable you are interested in and press \n"show graph". \nPlease keep in mind that the data might take a moment to load. \nThank you for using the Environmental parser.')

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

    date = date_combo.get()

    date_tar = Path(f'./{date}.tar.gz')
    uncompressed_tar = Path(f'./{date}/')

    if uncompressed_tar.is_dir():
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
            command = f'tar -xvf {date}.tar.gz'
            subprocess.call(command, shell = True)
        else:
            T.delete('1.0', END)
            T.insert(END, f'tar does not exist, will download, uncompress and prep {date} data. Press prep data again to test if loaded.')
            print("tar does not exist, will download and uncompress.")
            command = f'iget -rKTP -N 0 /iplant/home/shared/terraref/ua-mac/raw_tars/season_11_yr_2020/EnvironmentLogger/{date}.tar.gz'
            subprocess.call(command, shell = True)
            command = f'tar -xvf {date}.tar.gz'
            subprocess.call(command, shell = True)
            T.delete('1.0', END)
            T.insert(END, f'{date} data ready.')


def load_data():
        # time_start = "10:00" # Uncomment if want time beween timeframe
    # time_end = "23:00" # Uncomment if want time between timeframe

    global timeframe

    date = date_combo.get()
    
    list_all = glob.glob(f'./{date}/{date}*.json')

    # Set up empty dictionary and dataframe
    d = {}
    d_all = pd.DataFrame()

    ## Parse document
    for json_in in list_all:

        d = {}
        
        with open(json_in, 'r') as f:
            data = json.load(f)

            try:
                ## Extract required environmental info
                for i in range(len(data['environment_sensor_readings'])):

                    time = data["environment_sensor_readings"][i]["timestamp"]
                    sundir = data["environment_sensor_readings"][i]["weather_station"]["sunDirection"]["value"]
                    airp = data["environment_sensor_readings"][i]["weather_station"]["airPressure"]["value"]
                    bri = data["environment_sensor_readings"][i]["weather_station"]["brightness"]["value"]
                    relhum = data["environment_sensor_readings"][i]["weather_station"]["relHumidity"]["value"]
                    temp = data["environment_sensor_readings"][i]["weather_station"]["temperature"]["value"]
                    prec = data["environment_sensor_readings"][i]["weather_station"]["precipitation"]["value"]
                    wind_dir = data["environment_sensor_readings"][i]["weather_station"]["windDirection"]["value"]
                    wind_vel = data["environment_sensor_readings"][i]["weather_station"]["windVelocity"]["value"]
                    par = data["environment_sensor_readings"][i]["sensor par"]["value"]
                    co2 = data["environment_sensor_readings"][i]["sensor co2"]["value"]
                    
                    ## Add info to dictionary
                    d[i] = {
                    'Time' : time,
                    'Sun Direction' : sundir,
                    'Air Pressure': airp,
                    'Brightness': bri,
                    'Precipitation': prec,
                    'Relative humidity': relhum,
                    'Temperature': temp,
                    'Wind direction': wind_dir,
                    'Wind velocity': wind_vel,
                    'Photosynthetically active radiation': par,
                    'Co2': co2 
                    }
                
                ## Dictionary to dataframe
                df = pd.DataFrame.from_dict(d, orient='index')

                ## Merge all dataframes
                d_all = d_all.append(df)
                print(len(d_all))

            except:
                print("oops, something went wrong. Check that the date exists.")

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
    T.insert(tk.END, 'Instructions: this is the Environmental parser for the gantry scanalyzer data. Please select the day you are interested in viewing and select \n"prep data"; This will ensure data is downloaded and uncompressed - \nPlease give up to 10 minutes to donwload and uncompress your data, \ndepending on your internet connection. \nWhen data is ready, press "load data", please wait up to 1-2minutes. \nOnce loaded choose "day median" to view median of all collected \nenvironmental variables. \nIf you are interested in a specific data at a specific time, \nselect which environmental variable you are interested in and press \n"show graph". \nPlease keep in mind that the data might take a moment to load. \nThank you for using the Environmental parser.')

####################
# Buttons, placement

load_btn = Button(root, text = "load data", command = load_data)
load_btn.pack()

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
date_lbl.place(x=47, y= 45) # date label
date_combo.place(x=45, y=65) # date combobox
prep_button.place(x= 5, y=90) # prep data button
load_btn.place(x=90, y=90) # load data button
text_btn.place(x=175, y= 90) # day data text button 
env_lbl.place(x=20, y= 120) # env label
env_combo.place(x=45, y= 160) # env combobox
Graph_button.place(x=90, y= 185) # graph button
T.place(x=267, y=5) # Text box

root.mainloop()
