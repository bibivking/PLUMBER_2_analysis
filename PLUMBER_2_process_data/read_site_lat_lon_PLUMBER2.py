#!/usr/bin/env python

"""
Read the lat and lon information for each PLUMBER 2 sites

"""
__author__  = "Mengyuan Mu"
__version__ = "1.0 (22.11.2022)"

import os
import sys
import glob
import numpy as np
import netCDF4 as nc


file_path  = "/srv/ccrc/LandAP/z5218916/cable/runs/PLUMBER_2_runs/CABLE_GW_PLUMBER2/PLUMBER2_Phase_1/"
file_names = glob.glob(os.path.join(file_path, "*.nc"))

MSWEP_path = "/srv/ccrc/LandAP/z5218916/data/MSWEP_v280_past/Annual"

f_all_sh   = open("./sh_file/run_all_site.sh", "w")
f_all_sh.write("#!/bin/bash\n")
f_all_sh.write("  \n")

for file_name in file_names:
    
    site  = os.path.basename(file_name).split("_")[0]

    fname = nc.Dataset(file_name)
    lat   = fname.variables['latitude'][0,0]
    lon   = fname.variables['longitude'][0,0]

    # cdo outputtab
    f     = open("./sh_file/%s_%s_%s.sh" % (site,str(lat),str(lon)), "w")
    f.write("#!/bin/bash\n")
    f.write("  \n")

    for yr in np.arange(1979,2021):
        print('cdo -outputtab,date,value -remapnn,"lon=%s_lat=%s" %s/%s.nc > ./csv/%s_%s.csv' 
                %(str(lon), str(lat), MSWEP_path, str(yr), site, str(yr)))
        f.write('cdo -outputtab,date,value -remapnn,"lon=%s_lat=%s" %s/%s.nc > ./csv/%s_%s.csv \n' 
                %(str(lon), str(lat), MSWEP_path, str(yr), site, str(yr)))
    f.close()

    # write sh command
    f_all_sh.write('./%s_%s_%s.sh \n'% (site,str(lat),str(lon)))

f_all_sh.close()