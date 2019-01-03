#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 2 of the ITD paper: seasonal cycles of sea ice extent and volume

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import interp1d
import os

# Import functions
from seaice_commondiags import *

# Import directory location
exec(open("info.py"))

# Some color functions (https://gist.github.com/matthewkremer/3295567)
def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) / 255.0 for i in range(0, hlen, hlen/3))

# Years
yearb, yeare = 1995, 2014
years = np.arange(yearb, yeare + 1)
n_years = len(years)

# Experiments to plot
exps   = ["REF", "EXP_015", "EXP_016", "EXP_014", "EXP_017", "EXP_018", "EXP_019"] 
n_exps = len(exps)

labels = ["REF",     "S1.01",   "S1.03",   "S1.05",   "S1.10",   "S1.30",   "S1.50"]
colors = ["#434343", "#957DAD", "#2C1392", "#83AE44", "#FFD500", "#FFB661", "#FF6961"]

# Read NEMO grid
gridfile = repo + "/" + "mesh_mask_nemo.N3.6_ORCA1L75.nc"
f = Dataset(gridfile, mode = "r")
e1t = f.variables["e1t"][:]
e2t = f.variables["e2t"][:]
cellarea = e1t * e2t
lat = f.variables["gphit"][:]
lon = f.variables["glamt"][:]
mask= f.variables["tmaskutil"][:]
f.close()


diags = ["extent", "volume"]
units = ["10$^6$ km$^2$", "10$^3$ km$^3$"]
n_diags = len(diags)

regions =   ["Arctic", "Antarctic"]
n_regions = len(regions)


data = np.empty((n_diags, n_regions, n_exps, n_years * 12))
data[:] = np.nan
# Seasonal cycles
cycles = np.empty((n_diags, n_regions, n_exps, 12))
cycles[:] = np.nan

for j_e, e in enumerate(exps):
    if e == "REF":
        for j_d, d in enumerate(diags):
            for j_r, r in enumerate(regions):
                if r == "Arctic":
                    shortname = "nh"
                elif r == "Antarctic":
                    shortname = "sh"
                else: 
                    sys.exit("(fig2) region unknown")

            if d == "extent":
                filein = repo + "/REF/" + "siconc_SImon_OSI-409a_r1i1p1_197901-201512_nh.nc"
                f = Dataset(filein, mode = "r")
                siconc = f.variables["siconc"][:]
                mask_or= f.variables["sftof"][:]
                cellarea_or=f.variables["areacello"][:]
                f.close()

                diag =  compute_extent(siconc[:, :, :], cellarea_or[0, :, :], threshold = 15.0, mask = mask_or[0, :, :])

                data[j_d, j_r, j_e, (year - yearb) * 12 : (year - yearb) * 12 + 12] = diag[(yearb - 1979) * 12:(yeare - 1979) * 12 + 12]
    else: # Model data

        # 1. Load the data
        for year in years:
            filein = repo + "/" + e + "/" + e + "_1m_" + str(year) + "0101_" + str(year) + "1231_icemod.nc"
            f = Dataset(filein, mode = "r")
            siconc = f.variables["siconc"][:] * 100.0 #Conversion to %
            sivolu = f.variables["sivolu"][:]
            f.close()
    
            # Compute diagnostics
            for j_r, r in enumerate(regions):
                if r == "Arctic":
                    maskregion = (lat > 0.0)
                elif r == "Antarctic":
                    maskregion = (lat < 0.0)
                else:
                    sys.exit("(fig2) region unknown")
    
                for j_d, d in enumerate(diags):
                    if d == "extent":
                        diag = compute_extent(siconc, cellarea, threshold = 15.0, mask = (maskregion * mask))
                    elif d == "volume":
                        diag = compute_volume(sivolu, cellarea,                   mask = (maskregion * mask))
                    else:
                        sys.exit("(fig2) unknown diag")
    
                    data[j_d, j_r, j_e, (year - yearb) * 12 : (year - yearb) * 12 + 12] = diag
    

    # Compute seasonal cycles
    for j_r, r in enumerate(regions):
        for j_d, d in enumerate(diags):
            series = data[j_d, j_r, j_e, :]  
            cycles[j_d, j_r, j_e, :] = np.array([np.mean(series[m::12]) for m in np.arange(12)])

# Plots
fig = plt.figure(figsize = (10, 10))

j_plot = 1

for j_r, r in enumerate(regions):
    for j_d, d in enumerate(diags):
        plt.subplot(n_regions, n_diags, j_plot)
        for j_e, e in enumerate(exps):
            # Trick: appending the January after December and December before January for 
            #        better visual effect
            series = cycles[j_d, j_r, j_e, :]
            newseries = np.append(np.append(series[-1], series), series[0])

            newtime = np.arange(0, 12 + 2)
            f = interp1d(newtime, newseries, kind = 'cubic')

            hrtime = np.arange(0, 12 + 1, 0.1)

            plt.plot(hrtime, f(hrtime), color = colors[j_e], lw = 3, label = labels[j_e])

            # Plot data lighter
            rgb = hex_to_rgb(colors[j_e])
            rgb_dark = [0.5 + 0.5 * rg for rg in rgb]
            plt.scatter(newtime, newseries, 50, marker = "*", color = rgb, zorder = 1000, edgecolor = "white", linewidth = 0.2)

        ylim = plt.gca().get_ylim()

        for m in range(12):
          if m % 2 == 0: 
            col = [0.9, 0.9, 0.9]
          else:
            col = [1.0, 1.0, 1.0]

          plt.fill((m + 0.5, m + 1.5, m + 1.5, m + 0.5), (0.0, 0.0, 1e9, 1e9), color = col, zorder = 0)


        plt.title(r + " sea ice " + d)
        plt.xlim(0.5, 12.5)
        plt.ylim(ylim)
        plt.xticks(range(1, 12 + 1), ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])   
        plt.gca().tick_params(bottom = "off")
        plt.gca().set_ylim(bottom = 0)
        plt.ylabel(units[j_d])
        plt.legend()
   
        j_plot += 1

plt.savefig("./fig2.png", dpi = 300)
plt.close("all")
