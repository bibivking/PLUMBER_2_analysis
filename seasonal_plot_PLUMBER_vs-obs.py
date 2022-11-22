#!/usr/bin/env python

"""
Plot visual benchmark (average seasonal cycle) of old vs new model runs.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (18.10.2017)"

import matplotlib.pyplot as plt
import sys
import datetime as dt
import pandas as pd
import numpy as np
from matplotlib.ticker import FixedLocator
import os
import xarray as xr
import netCDF4 as nc


def main(n, ax, fname0, fname1, fname2, fname3, site, vars):

    df_0 = read_cable_file(fname0,fname1,vars)
    df_0 = resample_to_seasonal_cycle(df_0,fname0,vars)
    df_1 = read_cable_file(fname1,fname1,vars)
    df_1 = resample_to_seasonal_cycle(df_1,fname1,vars)
    df_2 = read_cable_file(fname2,fname2,vars)
    df_2 = resample_to_seasonal_cycle(df_2,fname2,vars)
    df_3 = read_cable_file(fname3,fname3,vars)
    df_3 = resample_to_seasonal_cycle(df_3,fname3,vars)

    ax.plot(df_0[vars], c="Black", lw=1., ls="-",label="obs")
    ax.plot(df_1[vars], c="red", lw=1., ls="-",label="gw_on")
    ax.plot(df_2[vars], c="DodgerBlue", lw=1., ls="-",label="gw_off")
    ax.plot(df_3[vars], c="green", lw=1., ls="-",label="gw_norecharge")

#    if vars == "GPP":
#        labels = "GPP (g C m$^{-2}$ d$^{-1}$)"
#    if vars == "Qle":
#        labels ="Qle (W m$^{-2}$)"
#    if vars == "Qh":
#        labels ="Qh (W m$^{-2}$)"
#    if vars == "Qg":
#        labels ="Qg (W m$^{-2}$)"
#    if vars == "Rnet":
#        labels ="Rnet (W m$^{-2}$)"
    labels ="%s" %site
    ax.set_title(labels, fontsize=12)
    if n < 15 and n !=12:
       plt.setp(ax.get_xticklabels(), visible=False)
#    xtickagaes_minor = FixedLocator([2, 3, 4, 5, 7, 8, 9, 10, 11])
#    ax.set_xticks([1, 6, 12])
#    ax.xaxis.set_minor_locator(xtickagaes_minor)
#    ax.set_xticklabels(['Jan', 'Jun', 'Dec'])
    if n > 14 or n == 12:
#        plt.setp(ax.get_xticklabels(), visible=False)
       xtickagaes_minor = FixedLocator([2, 3, 4, 5, 7, 8, 9, 10, 11])
       ax.set_xticks([1, 6, 12])
       ax.xaxis.set_minor_locator(xtickagaes_minor)
       ax.set_xticklabels(['Jan', 'Jun', 'Dec'])
    if n == 0:
       ax.legend(numpoints=1, loc="best")

def read_cable_file(fname,ftime, vars):

    ft = nc.Dataset(ftime)
    time = nc.num2date(ft.variables['time'][:],
                        ft.variables['time'].units)
    f = nc.Dataset(fname)
    df = pd.DataFrame(f.variables[vars][:,0], columns=[vars])

    df['dates'] = time
    df = df.set_index('dates')

    return df

def resample_to_seasonal_cycle(df, fname, vars):

    UMOL_TO_MOL = 1E-6
    MOL_C_TO_GRAMS_C = 12.0
    SEC_2_DAY = 86400.

    if vars == "GPP":
        df['GPP'] *= UMOL_TO_MOL * MOL_C_TO_GRAMS_C * SEC_2_DAY

    method = {vars :'mean'}

    df = df.resample("M").agg(method).groupby(lambda x: x.month).mean()
    df['month'] = np.arange(1,13)

    return df

if __name__ == "__main__":


    fig1 = plt.figure(figsize=(9,6))
    fig1.subplots_adjust(hspace=0.05)
    fig1.subplots_adjust(wspace=0.20)

#    fig2 = plt.figure(figsize=(6,6))
#    fig2.subplots_adjust(hspace=0.05)
#    fig2.subplots_adjust(wspace=0.05)

    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['font.size'] = 8
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8

    plot_dir = "plots"
    if not os.path.exists(plot_dir):
           os.makedirs(plot_dir)


    site_namelist = ["Amplero","Blodgett","Bugac","Espirra",\
                     "FortPeck","Harvard","Hesse","Howlandm",\
                     "Hyytiala","Kruger","Loobos","Merbleue",\
                     "Mopane","Palang","Sylvania","Tumba",\
                     "UniMich","Howard"]
    #,"UniMich"]

    case_name = "MD_elev_orig_std_avg-sand_ssgw-off"#_Haverd2013"

    vars = "Qle"
    # "Qle", "Qh", "GPP", "Qg", "Rnet"

    for n,site in enumerate(site_namelist):
        print(n)
        print(site)
        fname0 = "/srv/ccrc/data45/z3509830/CABLE_runs/Inputs/PLUMBER_sites/flux/%sFluxnet.1.4_flux.nc" %(site)
        print(fname0)
        fname1 = "/srv/ccrc/data25/z5218916/cable/runs/PLUMBER_gw_on_unify_para/outputs/%s_GW_on_%s_out.nc" %(site,case_name)
        print(fname1)
        fname2 = "/srv/ccrc/data25/z5218916/cable/runs/PLUMBER_gw_off_unify_para/outputs/%s_GW_off_%s_out.nc" %(site,case_name)
        print(fname2)
        fname3 = "/srv/ccrc/data25/z5218916/cable/runs/PLUMBER_gw_on_no_aquifer_influence_unify_para/outputs/%s_GW_on_%s_out.nc" %(site,case_name)
        print(fname3)
        
        if n <16:
            ax1 = fig1.add_subplot(5,4,(n+1))
        else:
            ax1 = fig1.add_subplot(5,4,(n+2))
        main(n, ax1, fname0, fname1, fname2, fname3, site, vars)

        if n == 17:
            plt.show()
            fig1.savefig(os.path.join(plot_dir, "seasonal_%s_%s.png" %(vars,case_name)), bbox_inches='tight',
                    pad_inches=0.1,dpi=300)
            del ax1
            del fig1
