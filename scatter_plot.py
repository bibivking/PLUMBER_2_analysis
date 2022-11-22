#!/usr/bin/env python

"""
Plot visual benchmark (average seasonal cycle) of old vs new model runs.

That's all folks.
"""
__author__  = "Mengyuan Mu"
__version__ = "1.0 (18.10.2017)"


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

def plot_scatters(file_name, var_names):

    case_name = os.path.basename(file_name).split("_")[0]
    fname     = nc.Dataset(file_name)
    time      = nc.num2date(fname.variables['time'][:],fname.variables['time'].units)
    vars_tmp  = np.zeros((len(var_names),len(time)))

    for i,var_name in enumerate(var_names):
        if var_name in ["Rainf","Snowf","Evap","TVeg","ESoil","ECanop", "Qs","Qsb","Qrecharge"]:
            vars_tmp[i,:] = fname.variables[var_name][:,0,0]*30*60
        elif var_name in ["Tair","VegT","RadT","CanT",]:
            vars_tmp[i,:] = fname.variables[var_name][:,0,0]-273.15
        elif var_name in ["SoilTemp","SoilMoist"]:
            vars_tmp[i,:] = np.mean(fname.variables[var_name][:,:,0,0],axis=1)
        elif var_name in ["GPP", "NPP", "NEE",]:
            vars_tmp[i,:] = fname.variables[var_name][:,0,0]* 0.000001*12*30*60 # half hourly
        else:
            vars_tmp[i,:] = fname.variables[var_name][:,0,0]
    # set the number of panels
    var_sum          = len(var_names)
    sqrt_var_sum     = math.sqrt(var_sum)
    ceil_sq_var_sum  = math.ceil(sqrt_var_sum)
    print("ceil_sq_var_sum",ceil_sq_var_sum)

    # start plotting
    fig, axs = plt.subplots( nrows=ceil_sq_var_sum, ncols=ceil_sq_var_sum, figsize=[15,12],sharex=True, sharey=False, squeeze=True)
    # fig.subplots_adjust(hspace=0.05, wspace=0.20)

    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['font.size'] = 8
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8    

    """
        UMOL_TO_MOL = 1E-6
        MOL_C_TO_GRAMS_C = 12.0
        SEC_2_DAY = 86400.

        if vars == "GPP":
            df['GPP'] *= UMOL_TO_MOL * MOL_C_TO_GRAMS_C * SEC_2_DAY

        method = {vars :'mean'}
        df = df.resample("M").agg(method)
    """

    for i,var_name in enumerate(var_names):
        row_index = int(i / ceil_sq_var_sum)
        col_index = int(i % ceil_sq_var_sum)
        print(var_name," row=",row_index," col=",col_index)
        if var_name in ["GPP", "NPP", "NEE",]:
            label = var_name+" (g C m$^{-2}$ d$^{-1}$)"
        elif var_name in ["Qle","Qh","Qg","Rnet","SWdown","LWdown"]:
            label = var_name+" (W m$^{-2}$)"
        elif var_name in ["Tair","VegT","RadT","CanT",]:
            label = var_name+" ($^o$C)"
        elif var_name in ["Rainf","Snowf","Evap","TVeg","ESoil","ECanop", "Qs","Qsb","Qrecharge"]:
            label = var_name+" (mm)"
        elif var_name in ["WatTable"]:
            label = var_name+" (m)"
        else:
            label = var_name

        # plot = axs[row_index,col_index].plot(vars_tmp[i,:], c="blue", lw=1., ls="-")#,label="obs")#.rolling(window=15).mean()
        plot = axs[row_index,col_index].scatter(vars_tmp[0,:],vars_tmp[i,:], c="blue", lw=1., ls="-")#,label="obs")#.rolling(window=15).mean()
        axs[row_index,col_index].set_title(var_names[i]+" vs "+var_names[0], fontsize=8)
        # axs.legend(numpoints=1, loc="best")

        # plot.set_title(case_name, fontsize=12)
        # plt.setp(axs.get_xticklabels(), visible=False)
        fig.savefig( "./plots/time_series_%s.png" % case_name, bbox_inches='tight',pad_inches=0.1,dpi=300)

if __name__ == "__main__":

    file_path  = "/srv/ccrc/LandAP/z5218916/cable/runs/PLUMBER_2_runs/CABLE_GW_PLUMBER2_Aus2/outputs"
    #"/srv/ccrc/LandAP/z5218916/cable/runs/PLUMBER_2_runs/CABLE_GW/outputs"
    file_names = glob.glob(os.path.join(file_path, "*.nc"))
    var_names  = [ "Tair", "SoilMoist", "SWdown", "Rainf","LAI", "Snowf","LWdown","Qair","Wind","PSurf",
                    "Evap","TVeg","ESoil","ECanop", "Qs","Qsb","Qrecharge",
                    "Fwsoil", "WatTable",
                    "Qle", "Qh", "Qg", "Rnet", "LWnet", "SWnet",
                    "VegT","RadT","CanT",
                    "GPP", "NPP", "NEE",
                    "SoilTemp",
                    "Ebal","Wbal",
                   ]
    for i,file_name in enumerate(file_names):
        plot_scatters(file_name,var_names)
        
