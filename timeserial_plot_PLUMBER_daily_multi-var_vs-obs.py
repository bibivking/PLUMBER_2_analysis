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


def main(site, fname0, fname1, fname2, fname3 = None, fname4 = None):

    df_0 = read_cable_file(fname0,fname2)
    df_0 = resample_to_seasonal_cycle(df_0,fname0)

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

#    fig = plt.figure(figsize=(9,6))
#    fig.subplots_adjust(hspace=0.05)
#    fig.subplots_adjust(wspace=0.20)

    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['font.size'] = 8
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8

    ax1 = fig.add_subplot(4,5,1)
    ax2 = fig.add_subplot(4,5,2)
    ax3 = fig.add_subplot(4,5,3)
    ax4 = fig.add_subplot(4,5,4)
    ax5 = fig.add_subplot(4,5,5)
    ax6 = fig.add_subplot(4,5,6)
    ax7 = fig.add_subplot(4,5,7)
    ax8 = fig.add_subplot(4,5,8)
    ax9 = fig.add_subplot(4,5,9)
    ax10 = fig.add_subplot(4,5,10)
    ax11 = fig.add_subplot(4,5,11)
    ax12 = fig.add_subplot(4,5,12)
    ax13 = fig.add_subplot(4,5,13)
    ax14 = fig.add_subplot(4,5,14)
    ax15 = fig.add_subplot(4,5,15)
    ax16 = fig.add_subplot(4,5,16)
    ax17 = fig.add_subplot(4,5,17)
    ax18 = fig.add_subplot(4,5,18)
    ax19 = fig.add_subplot(4,5,19)
    ax20 = fig.add_subplot(4,5,20)

    axes = [\
            ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8,\
            ax9, ax10, ax11, ax12, ax13, ax14,\
            ax15, ax16, ax17, ax18, ax19, ax20\
           ]
    vars = [\
            "Qh","Rainf","Qle","TVeg","ESoil", \
            "CanopInt","Fwsoil","Qs","Qsb","Qrecharge",  \
            "SoilMoist1","SoilMoist2","SoilMoist3","SoilMoist4","SoilMoist5",\
            "SoilMoist6","GWMoist", "SatFrac", "WatTable", "SWE"\
           ] 
#"SnowDepth"
# "SnowMelt",
#"Ebal",
#ssnow%snowd
#ssnow%sdepth
#ssnow%smelt
    f0 = "obs"
    f1 = "gw_on"
    f2 = "gw_off"
    f3 = "gw_no_aquifer"
    f4 = "SoilMoist"
    f5 = "SoilMoistIce"

    for a, v in zip(axes, vars):
        print(v)
        if (v == "Rainf"):
            print(len(df_0[v]))
            a.plot(df_0[v], c="Black", lw=1.0, ls="-",
                   label="%s" %(f0) ) #.rolling(window=7).mean()
        elif (v == "Qh" or v == "Qle"):
            a.plot(df_1[v].rolling(window=14).mean(), c="Black", lw=1.0, ls="-",
                   label="%s" %(f0) ) #
            a.plot(df_2[v].rolling(window=14).mean(), c="Red", lw=1.0, ls="-",
                   label="%s" %(f1) ) #.cumsum()
            a.plot(df_3[v].rolling(window=14).mean(), c="Blue", lw=1.0, ls="-",
                   label="%s" %(f2) ) #.cumsum()  
            a.plot(df_4[v].rolling(window=14).mean(), c="Green", lw=1.0, ls="-",
                   label="%s" %(f3) ) #.cumsum()                             
        elif (v == "Qrecharge" or v == "Qs" or v == "Qsb"):
            a.plot(df_2[v].cumsum(), c="Red", lw=1.0, ls="-",
                   label="%s" %(f1) ) #
            a.plot(df_3[v].cumsum(), c="Blue", lw=1.0, ls="-",
                   label="%s" %(f2) ) #.cumsum()
            a.plot(df_4[v].cumsum(), c="Green", lw=1.0, ls="-",
                   label="%s" %(f3) ) #.cumsum()
        elif ("SoilMoist" in v):
            a.plot(df_2[v].rolling(window=14).mean(), c="Red", lw=1.0, ls="-",
                   label="%s-%s" %(f1,f4) )
            a.plot(df_2["%sIce" %(v)].rolling(window=14).mean(), c="Orange", lw=1.0, ls="-",
                   label="%s-%s" %(f1,f5) )
            a.plot(df_3[v].rolling(window=14).mean(), c="Blue", lw=1.0, ls="-",
                   label="%s-%s" %(f2,f4) )
            a.plot(df_3["%sIce" %(v)].rolling(window=14).mean(), c="DodgerBlue", lw=1.0, ls="-",
                   label="%s-%s" %(f2,f5) )
            a.plot(df_4[v].rolling(window=14).mean(), c="Green", lw=1.0, ls="-",
                   label="%s-%s" %(f3,f4) )
            a.plot(df_4["%sIce" %(v)].rolling(window=14).mean(), c="LightGreen", lw=1.0, ls="-",
                   label="%s-%s" %(f3,f5) )
        elif (v == "WatTable" or v ==  "GWMoist" or v == "SatFrac"):
            a.plot(df_2[v].rolling(window=14).mean(), c="Red", lw=1.0, ls="-",
                   label="%s" %(f1) ) #.cumsum()
            a.plot(df_4[v].rolling(window=14).mean(), c="Green", lw=1.0, ls="-",
                   label="%s" %(f3) ) #.cumsum()
        else:
            a.plot(df_2[v].rolling(window=14).mean(), c="Red", lw=1.0, ls="-",
                   label="%s" %(f1) ) #.cumsum()
            a.plot(df_3[v].rolling(window=14).mean(), c="Blue", lw=1.0, ls="-",
                   label="%s" %(f2) ) #.cumsum()
            a.plot(df_4[v].rolling(window=14).mean(), c="Green", lw=1.0, ls="-",
                   label="%s" %(f3) ) #.cumsum()

    labels = [\
              "Qh(W/m$^{2}$)",\
              "Rainf(mm)",\
              "Qle(W/m$^{2}$)", \
              "TVeg(mm)", \
              "ESoil(mm)",\
              "CanopInt(mm)",    \
              "Fwsoil", \
              "Qs acmlt(mm)",   \
              "Qsb acmlt(mm)",  \
              "Qrecharge acmlt(mm)",\
              "layer1(m$^{3}$ m$^{-3}$)",\
              "layer2(m$^{3}$ m$^{-3}$)",\
              "layer3(m$^{3}$ m$^{-3}$)",\
              "layer4(m$^{3}$ m$^{-3}$)",\
              "layer5(m$^{3}$ m$^{-3}$)",\
              "layer6(m$^{3}$ m$^{-3}$)",\
              "GWMoist(m$^{3}$ m$^{-3}$)",  \
              "SatFrac",\
              "WatTable(m)",  \
              "SWE(mm)"    \
              ]
# "SnowDepth(mm)"
# "SnowMelt(mm)", \
# "Ebal(W/m$^{2}$)",\

    for a, l in zip(axes, labels):
        a.set_ylabel(l, fontsize=8)

    for i,a in enumerate(axes):
        if i < 20:
            plt.setp(a.get_xticklabels(), visible=False)
    ax1.legend(numpoints=1, loc="best")
    ax2.legend(numpoints=1, loc="best")
    ax3.legend(numpoints=1, loc="best")
    ax16.legend(numpoints=1, loc="best")

    if site is None:
        print("None site")
        plt.show()
    else:
        plt.show()
        plot_dir = "plots"
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        fig.savefig(os.path.join(plot_dir, "PLUMBER-%s-daily_multi-var_vs_obs_standard" %(site)), bbox_inches='tight',
                    pad_inches=0.1)
       # format='pdf',

def read_cable_file(fname, ftime):

#    step_s = 0     #44640
#    step_e = 70128 #44784
#    GWdz   = 18.75098 # for Sylvania

    ft = nc.Dataset(ftime)
    time = nc.num2date(ft.variables['time'][:],
                        ft.variables['time'].units)
    f = nc.Dataset(fname)

    if "met" in fname:
        df = pd.DataFrame(f.variables['Rainf'][:,0], columns=['Rainf'])
    elif "flux" in fname:
        df = pd.DataFrame(f.variables['Qh'][:,0], columns=['Qh'])
        df['Qle'] = f.variables['Qle'][:,0]        
    else:
        df = pd.DataFrame(f.variables['Qh'][:,0], columns=['Qh'])	
        df['Qle']      = f.variables['Qle'][:,0]
        df['TVeg'] = f.variables['TVeg'][:,0]
        df['ESoil'] = f.variables['ESoil'][:,0]
        df['Qs'] = f.variables['Qs'][:,0]
        df['Qsb'] = f.variables['Qsb'][:,0]
        df['Qrecharge'] = f.variables['Qrecharge'][:,0]
#        df['SnowMelt']  = f.variables['SnowMelt'][:,0]
        df['WatTable']  = f.variables['WatTable'][:,0]
        df['GWMoist']   = f.variables['GWMoist'][:,0]#*GWdz*1000.

        df['SoilMoist1'] = f.variables['SoilMoist'][:,0,0]#*0.022*1000.
        df['SoilMoist2'] = f.variables['SoilMoist'][:,1,0]#*0.058*1000.
        df['SoilMoist3'] = f.variables['SoilMoist'][:,2,0]#*0.154*1000.
        df['SoilMoist4'] = f.variables['SoilMoist'][:,3,0]#*0.409*1000.
        df['SoilMoist5'] = f.variables['SoilMoist'][:,4,0]#*1.085*1000.
        df['SoilMoist6'] = f.variables['SoilMoist'][:,5,0]#*2.872*1000.

        df['SoilMoist1Ice'] = f.variables['SoilMoistIce'][:,0,0]#*0.022 +\
        df['SoilMoist2Ice'] = f.variables['SoilMoistIce'][:,1,0]#*0.058 +\
        df['SoilMoist3Ice'] = f.variables['SoilMoistIce'][:,2,0]#*0.154 +\
        df['SoilMoist4Ice'] = f.variables['SoilMoistIce'][:,3,0]#*0.409 +\
        df['SoilMoist5Ice'] = f.variables['SoilMoistIce'][:,4,0]#*1.085 +\
        df['SoilMoist6Ice'] = f.variables['SoilMoistIce'][:,5,0]#*2.872)*1000.

        df['SatFrac']  = f.variables['SatFrac'][:,0]

        df['CanopInt']  = f.variables['CanopInt'][:,0]
        #df['SnowDepth'] = f.variables['SnowDepth'][:,0]*1000.
        df['SWE'] = f.variables['SWE'][:,0]
        df['Fwsoil']      = f.variables['Fwsoil'][:,0]

    df['dates'] = time
    df = df.set_index('dates')

    return df

def resample_to_seasonal_cycle(df, fname, OBS=False):

    SEC_2_HLFHOUR = 1800.
    ICE_2_WATER   = 0.9167

    if "outputs" in fname:
        # kg/m2/s -> mm/30min
#        df['Evap']  *= SEC_2_HLFHOUR
        df['TVeg'] *= SEC_2_HLFHOUR
        df['ESoil'] *= SEC_2_HLFHOUR
        df['Qs']    *= SEC_2_HLFHOUR
        df['Qsb']   *= SEC_2_HLFHOUR
        df['Qrecharge'] *= SEC_2_HLFHOUR
#        df['SnowMelt'] *= SEC_2_HLFHOUR

        #ice->water m3/m3->mm, Ice density is 0.9167 g/cm3
#        df['SoilMoist1Ice'] *= ICE_2_WATER
#        df['SoilMoist2Ice'] *= ICE_2_WATER
#        df['SoilMoist3Ice'] *= ICE_2_WATER
#        df['SoilMoist4Ice'] *= ICE_2_WATER
#        df['SoilMoist5Ice'] *= ICE_2_WATER
#        df['SoilMoist6Ice'] *= ICE_2_WATER

        method = {'Qh':'mean','Fwsoil':'mean','Qle':'mean','TVeg':'sum',\
                  'ESoil':'sum','Qs':'sum','Qsb':'sum','Qrecharge':'sum', \
                  'WatTable':'mean','SoilMoist1':'mean',\
                  'SoilMoist2':'mean','SoilMoist3':'mean','SoilMoist4':'mean',\
                  'SoilMoist5':'mean','SoilMoist6':'mean','SoilMoist1Ice':'mean',\
                  'SoilMoist2Ice':'mean','SoilMoist3Ice':'mean','SoilMoist4Ice':'mean',\
                  'SoilMoist5Ice':'mean','SoilMoist6Ice':'mean','GWMoist':'mean',\
                  'SatFrac':'mean','CanopInt':'mean','SWE':'mean'}
#        'SnowDepth':'mean'                  	
#        'SnowMelt':'sum',
        df = df.resample("D").agg(method)

    elif "met" in fname:
        # mm/s -> mm/30min
        df['Rainf'] *= SEC_2_HLFHOUR

        method = {'Rainf':'sum'}
        df = df.resample("D").agg(method)
             #'Wbal':'mean'
             
    elif "flux" in fname:

        method = {'Qh':'mean','Qle':'mean'}
        df = df.resample("D").agg(method)
             #'Wbal':'mean'

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
#    case_name1 = "MD_elev_orig_std_cpr"
#    case_name2 = "MD_elev_orig_std"

    for n,site in enumerate(site_namelist):
        print(n)
        print(site)
        fname0 = "/srv/ccrc/data45/z3509830/CABLE_runs/Inputs/PLUMBER_sites/met/%sFluxnet.1.4_met.nc" %(site)
        print(fname0)
        fname1 = "/srv/ccrc/data45/z3509830/CABLE_runs/Inputs/PLUMBER_sites/flux/%sFluxnet.1.4_flux.nc" %(site)
        print(fname1)
        fname2 = "%s/%s_GW_on_%s_out.nc" %(path_on, site, case_name) 
        print(fname2)
        fname3 = "%s/%s_GW_off_%s_out.nc" %(path_off, site, case_name)
        print(fname3)
        fname4 = "%s/%s_GW_on_%s_out.nc" %(path_no_aquifer,site,case_name)
        print(fname4)
        main(site, fname0, fname1, fname2, fname3, fname4)
