#!/usr/bin/env python

"""
Plot visual benchmark (average seasonal cycle) of old vs new model runs.

That's all folks.

Copied from /srv/ccrc/data25/z5218916/cable/runs/PLUMBER_runs/PLUMBER_gw_on_unify_para_using_cable-cpr/plot_timeseries_PLUMBER_vs-obs_y-day.py

"""

import matplotlib.pyplot as plt
import sys
import datetime as dt
import pandas as pd
import numpy as np
from matplotlib.ticker import FixedLocator
import os
import xarray as xr
import netCDF4 as nc


def main(site, fname1, fname2, fname3 = None, fname4 = None):

    df_1 = read_cable_file(fname1,fname2)
    df_1 = resample_to_seasonal_cycle(df_1,fname1)

    df_2 = read_cable_file(fname2,fname2)
    df_2 = resample_to_seasonal_cycle(df_2,fname2)

    if fname3 is not None:
        df_3 = read_cable_file(fname3,fname3)
        df_3 = resample_to_seasonal_cycle(df_3,fname3)

    if fname4 is not None:
        df_4 = read_cable_file(fname4,fname4)
        df_4 = resample_to_seasonal_cycle(df_4,fname4)
    # Note that: we cannot use itertools.accumulate here, because df_1 is from pd.dataframe. df_1 is not just a series of number but a DataFrame
    # import itertools as itl, itl.accumulate(df_1["WaterBal"])

    fig = plt.figure()

    fig = plt.figure(figsize=(9,6))
    fig.subplots_adjust(hspace=0.05)
    fig.subplots_adjust(wspace=0.20)

    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['font.size'] = 8
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8

    ax = fig.add_subplot(1,1,1)

    var = "Qle"

    f0 = "obs"
    f1 = "gw_on"
    f2 = "gw_off"
    f3 = "gw_no_aquifer"
    f4 = "SoilMoist"
    f5 = "SoilMoistIce"

    ax.plot(df_1[var].rolling(window=7).mean(), c="Black", lw=1.0, ls="-",
           label="%s" %(f0) ) #
    ax.plot(df_2[var].rolling(window=7).mean(), c="Red", lw=1.0, ls="-",
           label="%s" %(f1) ) #.cumsum()
    ax.plot(df_3[var].rolling(window=7).mean(), c="Blue", lw=1.0, ls="-",
           label="%s" %(f2) ) #.cumsum()
    ax.plot(df_4[var].rolling(window=7).mean(), c="Green", lw=1.0, ls="-",
           label="%s" %(f3) ) #.cumsum()

    label = "Qle(W/m$^{2}$)"

    ax.set_ylabel(label, fontsize=8)

    plt.setp(ax.get_xticklabels(), visible=True)
    ax.legend(numpoints=1, loc="best")

    if site is None:
        print("None site")
        plt.show()
    else:
        plt.show()
        plot_dir = "plots"
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        fig.savefig(os.path.join(plot_dir, "PLUMBER-%s-daily_multi-Qle_vs_obs_standard" %(site)), bbox_inches='tight',
                    pad_inches=0.1)
       # format='pdf',

def read_cable_file(fname, ftime):

    ft = nc.Dataset(ftime)
    time = nc.num2date(ft.variables['time'][:],
                       ft.variables['time'].units)
    f = nc.Dataset(fname)
    df = pd.DataFrame(f.variables['Qle'][:,0], columns=['Qle'])
    df['dates'] = time
    df = df.set_index('dates')

    return df

def resample_to_seasonal_cycle(df, fname, OBS=False):

    method = {'Qle':'mean'}
    df = df.resample("D").agg(method)
    return df

if __name__ == "__main__":

    site_namelist = ["Amplero","Blodgett","Bugac",\
                     "Espirra","FortPeck","Harvard","Hesse","Howard",\
                     "Howlandm","Hyytiala","Kruger","Loobos","Merbleue",\
                     "Mopane","Palang","Sylvania","Tumba","UniMich"]
    #,"ElSaler2","ElSaler",]

    path_on = "/srv/ccrc/data25/z5218916/cable/runs/PLUMBER_gw_on_unify_para/outputs"

    path_off = "/srv/ccrc/data25/z5218916/cable/runs/PLUMBER_gw_off_unify_para/outputs"

    path_no_aquifer = "/srv/ccrc/data25/z5218916/cable/runs/PLUMBER_gw_on_no_aquifer_influence_unify_para/outputs"

    case_name = "MD_elev_orig_std_avg-sand_ssgw-off"

    for n,site in enumerate(site_namelist):
        print(n)
        print(site)
        fname1 = "/srv/ccrc/data45/z3509830/CABLE_runs/Inputs/PLUMBER_sites/flux/%sFluxnet.1.4_flux.nc" %(site)
        print(fname1)
        fname2 = "%s/%s_GW_on_%s_out.nc" %(path_on, site, case_name)
        print(fname2)
        fname3 = "%s/%s_GW_off_%s_out.nc" %(path_off, site, case_name)
        print(fname3)
        fname4 = "%s/%s_GW_on_%s_out.nc" %(path_no_aquifer,site,case_name)
        print(fname4)
        main(site, fname1, fname2, fname3, fname4)
