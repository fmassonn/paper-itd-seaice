#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 3 of the ITD paper: winter patterns of sea ice thickness

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

import os

# Import functions
from seaice_commondiags import *

# Import directory location
exec(open("namelist.py"))

# Years
yearb, yeare = 1995, 2014
years = np.arange(yearb, yeare + 1)
n_years = len(years)

# Regions
regions = ["Arctic", "Antarctic"]
n_regions = len(regions)

# indices of experiments to plot (from namelist)
indices = [0, 1, 2, 3, 4, 5]

# Experiments to plot
exps   = [metadata[i][1] for i in indices]

reference = 2 #index of the reference for differences (pythonic)

n_exps = len(exps)

labels = [metadata[i][0] for i in indices]

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
        sivolu = f.variables["sivolu"][:]
        f.close()
        data[j_e, (year - yearb) * 12 : (year - yearb) * 12 + 12, :, :] = sivolu
    
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
        month = 3 - 1 # March, pythonic
        clevs = [0.0, 1.0, 2.0, 3.0, 4.0]
        clevs_diff = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9]#[-1.0, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1.0]
	myticks = [-0.9, -0.5, 0.0, 0.5, 0.9] 
    elif r == "Antarctic":
        m = Basemap(projection = "spstere", boundinglat = -60, lon_0 = 180, resolution = "l")
        month = 9 - 1 # September, pythonic
        clevs = [0.0,0.4, 0.8, 1.2, 1.6, 2.0]
        clevs_diff = [-0.5, -0.3, -0.1, 0.1, 0.3, 0.5]
        myticks = [-0.5, -0.3, 0.0, 0.3, 0.5]

    x, y = m(lon, lat)

    for j_e, e in enumerate(exps):
        plt.subplot(n_regions, n_exps, j_plot)
        m.drawcoastlines()
        m.fillcontinents(color = [0.7, 0.7, 0.7], lake_color = [1.0, 1.0, 1.0])

        if j_e == reference:
            levels = clevs
            datatoplot = cycles[j_e, month, :, :]
            cmap = plt.cm.gist_earth
            extend = "max"
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
        cbar.set_label("m")
        cbar.set_ticks(ticks)
        plt.title(title)
        #plt.tight_layout()
        j_plot += 1   

plt.tight_layout()
plt.savefig("./fig3.png", dpi = 300)
plt.close("all")
