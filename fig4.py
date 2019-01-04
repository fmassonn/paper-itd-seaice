#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 4 of the ITD paper: masks for computation of subsequent diagnostics
# Based on the reference experiment S1.05

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
indices = [2]

# Experiments to plot
exps   = [metadata[i][1] for i in indices]



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


data = np.empty((n_years * 12, ny, nx))
data[:] = np.nan

# Seasonal cycles  averages
cycles = np.empty((12, ny, nx))
cycles[:] = np.nan

# 1. Load the data
e = exps[0]

for year in years:
    filein = repo + "/" + e + "/" + e + "_1m_" + str(year) + "0101_" + str(year) + "1231_icemod.nc"
    f = Dataset(filein, mode = "r")
    siconc = f.variables["siconc"][:] * 100.0
    f.close()

    data[(year - yearb) * 12 : (year - yearb) * 12 + 12, :, :] = siconc
    
    # Compute seasonal cycles
    for m in range(12):
        cycles[m, :, :] = np.mean(data[m::12, :, :], axis = 0)


# Compute mask
maskzone = cycles > 99.0


# Plots
fig = plt.figure(figsize = (6, 3))

j_plot = 1

for j_r, r in enumerate(regions):

    # Create Basemap
    if r == "Arctic":
        m = Basemap(projection = "npstere", boundinglat = 65, lon_0 = 0,  resolution = "l")
        month = 3 - 1
    elif r == "Antarctic":
        m = Basemap(projection = "spstere", boundinglat = -60, lon_0 = 180, resolution = "l")
        month = 9 - 1

    x, y = m(lon, lat)

    plt.subplot(1, n_regions, j_plot)
    m.drawcoastlines()
    m.fillcontinents(color = [0.7, 0.7, 0.7], lake_color = [1.0, 1.0, 1.0])

    cs = m.contourf(x,           y,            maskzone[month, :, :], cmap = plt.cm.binary, levels = np.arange(-1, 2), latlon = False)
    # Second call to contourf, ignoring last row and column: a strange NEMO grid issue
    cs = m.contourf(x[:-1, :-1], y[:-1, :-1],  maskzone[month, :-1, :-1], cmap = plt.cm.binary, levels = np.arange(-1, 2), latlon = False)
    j_plot += 1   

plt.tight_layout()
plt.savefig("./fig4.png", dpi = 300)
plt.close("all")


# Save mask as NetCDF
# -------------------
fileout = repo + "./thermomask.nc"
# Create file
f = Dataset(fileout, mode = "w")
# Create dimensions
y   = f.createDimension("y", ny)
x   = f.createDimension("x", nx)
# Create variables

thermomask = f.createVariable("thermomask", np.float32, ("y", "x"))
# concatenate SH and NH masks
thermomask[:] = np.concatenate((maskzone[8, 0:146, :], maskzone[2, 146:, :]))

lons = f.createVariable('longitude', np.float32, ('y', 'x'))
lons[:] = lon

lats = f.createVariable('latitude', np.float32, ('y', 'x'))
lats[:] = lat

cellare = f.createVariable('areacello', np.float32, ('y', 'x'))
cellare.units = "m2"
cellare[:] = cellarea

sftof  = f.createVariable('sftof', np.float32, ('y', 'x'))
sftof[:] = mask

# Close
f.close()

