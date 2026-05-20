#!/usr/bin/env python

"""
summarize annual csv files into nc file

"""
__author__  = "Mengyuan Mu"
__version__ = "1.0 (22.11.2022)"

import os
import sys
import glob
import numpy as np
import pandas as pd
import netCDF4 as nc
import datetime as dt

# ==== get site names ====
file_path  = "/srv/ccrc/LandAP/z5218916/cable/runs/PLUMBER_2_runs/CABLE_GW_PLUMBER2/PLUMBER2_Phase_1/"
file_names = glob.glob(os.path.join(file_path, "*.nc"))
site_names = [ ]
for file_name in file_names:
    site_names.append(os.path.basename(file_name).split("_")[0])
    fname = nc.Dataset(file_name)
    Lat   = fname.variables['latitude'][0,0]
    Lon   = fname.variables['longitude'][0,0]
    fname.close()

print(site_names)

for site_name in site_names:
    print(site_name)   

    # ==== read csv data ====
    for yr in np.arange(1979,2021):
        csv_path   = "/srv/ccrc/LandAP/z5218916/script/PLUMBER_2_analysis/PLUMBER_2_process_data/csv/%s_%s.csv" %(site_name, str(yr))
        if yr == 1979:
            df     = pd.read_csv(csv_path,names = ['date','value'], skiprows=1, header=None, delim_whitespace=True,)# sep="    ",)
        else:
            df_tmp = pd.read_csv(csv_path,names = ['date','value'], skiprows=1, header=None, delim_whitespace=True,)#sep="    ",) 
            df = df.append(df_tmp)

    # # ==== calc Z score ====
    
    # # reshape to [year,day]
    df    = df.set_index('date')
    value = df['value'].values
    print(value)
    # df
    # # calc mean

    # # calc std
    
    # value    = df['value'].values
    # val_mean = np.nanmean(value)
    # val_std  = np.nanstd(value)









    # # set up nc file
    # ndim            = 1
    # ntime           = 15339 # 1979-01-02 - 2020-12-31
    
    # f               = nc.Dataset('./nc_files/%s.nc' %site_name, 'w', format='NETCDF4')
    # f.description   = '1979-2020 MSWEP precipitation at %s, created by MU Mengyuan' % (site_name)
    # f.history       = "Created by: %s" % (os.path.basename(__file__))
    # f.creation_date = "%s" % (dt.datetime.now())
    # f.Conventions   = "CF-1.0"

    # # set dimensions
    # f.createDimension('time', ntime)
    # f.createDimension('lat', ndim)
    # f.createDimension('lon', ndim)

    # # create variables
    # time           = f.createVariable('time', 'f4', ('time',))
    # time.units     = "days since 1979-01-01 00:00:00"
    # time.long_name = "time"
    # time.calendar  = "standard"
    # time[:]        = np.arange(2,ntime+2) # 2020-12-31 should be the ntime+1 day and +1 for arange

    # lat            = f.createVariable('lat', 'f4', ('lat',))
    # lat.long_name  = "latitude"
    # lat.units      = "degrees_north"
    # lat[:]         = Lat

    # lon            = f.createVariable('lon', 'f4', ('lon',))
    # lon.long_name  = "longitude"
    # lon.units      = "degrees_east"
    # lon[:]         = Lon

    # P              = f.createVariable('P', 'f4', ('time'))
    # P.long_name    = "precipitation"
    # P.units        = "mm d-1"
    # P._FillValue   = -9999.
    # P.missing_value= -9999.
    # P[:]           = df['value'].values
    # f.close()

    # # set to None
    # df   = None
    # time = None
    # lat  = None
    # lon  = None
    # P    = None



