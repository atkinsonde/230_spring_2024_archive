# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 01:37:17 2024

@author: Windows
"""

dir = "C:\\Users\\Windows\\Documents\\courses\\EOS_GEOG_230\\Lectures\\5_Binary_file_types\\"

#######  PART 1
fn = "test.b"

with open(dir+fn, "wb") as file:
    # byte format - recall the ASCII table
    byte_data = b"\x59\x56\x69\x63\x0D\x0A" # let's make something up ** NOTE THE b  
    file.write(byte_data)
    
### You must explicitly close the file!!
### the with statement automatically closes the file

# Have a look at what we wrote:
with open(dir+fn,"rb") as file:
    zz=file.read()
    print(zz)


#######  PART 2 write integers in binary form
import array

fn = "test_num.bin"
vals = [10,20,30,40,50]
data = array.array("B", vals) 

with open(dir+fn, "wb") as file:
    file.write(data.tobytes()) 

with open(dir+fn,"rb") as file:
    zz  = file.read()
    zzn = [x for x in zz]
    print(zzn)

#######  PART 3 write integers as strings in binary form
fn = "test_num_B.bin"
vals = ["10", "20", "30", "40", "50"]
#vals_b = [x.encode('utf-8') for x in vals ]

with open(dir+fn, "wb") as file:
    [file.write(x.encode('utf-8')) for x in vals] 

with open(dir+fn,"rb") as file:
    zz=file.read()
    print(zzn)

#######  PART 4  HDF read
import h5py
import pandas as pd
import numpy as np

dir_n = "C:\\Users\\Windows\\Documents\\courses\\EOS_GEOG_230\\Lectures\\5_Binary_file_types\\nimbus_hdf\\"
fn    = "NmHRIR1H.19660823_01-50-12_1332_002.hdf.xml"
nimbus_meta = pd.read_xml(dir_n+fn)
nimbus_meta.iloc[2,:]

fn = "NmHRIR1H.19660823_01-50-12_1332_002.hdf"

f = h5py.File(dir_n+fn, 'r')

f.keys()
f['Sat Longitude']

ds = np.array(f['HRIR-Temp']) # creates a numpy array from an HDF dataset
ds.shape
ds.dtype
ds[100,100]

#let's make a quick "heatmap" plot using some other python libraries:
from matplotlib import pyplot as plt
import seaborn as sns
sns.heatmap(ds)
plt.show()
# it seems there are some huge values in the set which are wrecking the plot

# we need to remove them using a conditional:
dsf = np.where(ds<350,ds,200)
sns.heatmap(dsf)
plt.show()

########  PART 5  netCDF read

import netCDF4 as nc

dir_nc = "C:\\Users\\Windows\\Documents\\courses\\EOS_GEOG_230\\Lectures\\5_Binary_file_types\\netCDF\\"
fn     = "vwnd.10m.1979.nc"

ds     = nc.Dataset(dir_nc+fn)
print(ds)

print(ds.variables.keys()) # get all variable names
ds['vwnd']
t1 = ds['vwnd'][0,:,:]

t1 = np.where(t1>-100,t1,-50)
sns.heatmap(t1)
plt.show()

t2 = ds['vwnd'][:,90,100]
pd.DataFrame(t2).plot()


#######  PART 6  Grib read

fn = "CMC_hrdps_west_TMP_TGL_2_ps2.5km_2020031312_P000-00.grib2"

import xarray as xr
ds = xr.load_dataset(dir_nc+fn, engine='cfgrib')
import cfgrib
