#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 6 of the ITD paper: summer patterns of sea ice concentratoin

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

import os

# Import functions
from seaice_commondiags import *

# Import directory location
exec(open("info.py"))

# Years
yearb, yeare = 1995, 2014
years = np.arange(yearb, yeare + 1)
n_years = len(years)

# Regions
regions = ["Arctic", "Antarctic"]
n_regions = len(regions)

# Experiments to plot
exps      = ["EXP_015", "EXP_016", "EXP_014", "EXP_017", "EXP_018", "EXP_019"] 
reference = 2 #index of the reference for differences (pythonic)

n_exps = len(exps)

labels = ["S1.01",   "S1.03",   "S1.05",   "S1.10",   "S1.30",   "S1.50"]

# Read NEMO grid
gridfile = repo + "/" + "mesh_mask_nemo.N3.6_ORCA1L75.nc"
f = Dataset(gridfile, mode = "r")
e1t = f.variables["e1t"][0, :, :]
e2t = f.variables["e2t"][0, :, :]
cellarea = e1t * e2t
lat = f.variables["gphit"][0, :, :]
lon = f.variables["glamt"][0, :, :]
mask= f.variables["tmaskutil"][0, :, :]
ny, nx = mask.shape
f.close()


data = np.empty((n_exps, n_years * 12, ny, nx))
data[:] = np.nan
# Seasonal cycles  averages
cycles = np.empty((n_exps, 12, ny, nx))
cycles[:] = np.nan

for j_e, e in enumerate(exps):
    # 1. Load the data
    for year in years:
        filein = repo + "/" + e + "/" + e + "_1m_" + str(year) + "0101_" + str(year) + "1231_icemod.nc"
        f = Dataset(filein, mode = "r")
        siconc = f.variables["siconc"][:] * 100.0 # to %
        f.close()
        data[j_e, (year - yearb) * 12 : (year - yearb) * 12 + 12, :, :] = siconc
    
    # Compute seasonal cycles
    for m in range(12):
        cycles[j_e, m, :, :] = np.mean(data[j_e, m::12, :, :], axis = 0)


# Plots
fig = plt.figure(figsize = (12, 6))

j_plot = 1

for j_r, r in enumerate(regions):

    # Create Basemap
    if r == "Arctic":
        m = Basemap(projection = "npstere", boundinglat = 65, lon_0 = 0,  resolution = "l")
        month = 8 - 1 # August, pythonic
        clevs = [0.0, 20, 40, 60, 80, 100]
        clevs_diff = [-90, -70, -50, -30, -10, 10, 30, 50, 70, 90]#[-1.0, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1.0]
	myticks = [-90, -50, 0, 50, 90] 
    elif r == "Antarctic":
        m = Basemap(projection = "spstere", boundinglat = -60, lon_0 = 180, resolution = "l")
        month = 2 - 1 # September, pythonic
        clevs = [0, 20, 40, 60, 80, 100]
        clevs_diff = [-50, -30, -10, 10, 30, 50]
        myticks = [-50, -30, 0, 30, 50]

    x, y = m(lon, lat)

    for j_e, e in enumerate(exps):
        plt.subplot(n_regions, n_exps, j_plot)
        m.drawcoastlines()
        m.fillcontinents(color = [0.7, 0.7, 0.7], lake_color = [1.0, 1.0, 1.0])

        if j_e == reference:
            levels = clevs
            datatoplot = cycles[j_e, month, :, :]
            cmap = plt.cm.Blues_r
            extend = "neither"
            title = labels[j_e]
            ticks = levels
        else:
            levels = clevs_diff
            datatoplot = cycles[j_e, month, :, :] - cycles[reference, month, :, :]
            cmap = plt.cm.RdBu_r
            extend = "both"
            title = labels[j_e] + "-" + labels[reference]
            ticks = myticks
            

        cs = m.contourf(x,          y,          datatoplot,     levels = levels, latlon = False, cmap = cmap, extend = extend)
        # Second call to contourf, ignoring last row and column: a strange NEMO grid issue
        cs = m.contourf(x[:-1,:-1], y[:-1,:-1], datatoplot[:-1,:-1], levels = levels, latlon = False, cmap = cmap, extend = extend)
        cbar = m.colorbar(cs, location = "bottom", pad = "5%")
        cbar.set_label("%")
        cbar.set_ticks(ticks)
        plt.title(title)
        #plt.tight_layout()
        j_plot += 1   

plt.tight_layout()
plt.savefig("./fig6.png", dpi = 300)
plt.close("all")
