#!/usr/bin/env python

"""
Read the lat and lon information for each PLUMBER 2 sites

"""
__author__  = "Mengyuan Mu"
__version__ = "1.0 (22.11.2022)"

import os
import sys
import glob
import math
import numpy as np
import xarray as xr
import netCDF4 as nc
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator


file_path  = "/srv/ccrc/LandAP/z5218916/cable/runs/PLUMBER_2_runs/CABLE_GW_PLUMBER2/PLUMBER2_Phase_1/"
file_names = glob.glob(os.path.join(file_path, "*.nc"))

for i,file_name in enumerate(file_names):
    site  = os.path.basename(file_name).split("_Met")[0]
    fname = nc.Dataset(file_name)
    lat   = fname.variables['latitude'][0,0]
    lon   = fname.variables['longitude'][0,0]
    f     = open("%s_%s_%s.sh" % (site,str(lat),str(lon)), "w")
    f.write("#!/bin/bash")
f.close()