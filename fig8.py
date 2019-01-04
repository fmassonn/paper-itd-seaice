#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 8 of the ITD paper: ITDs over masked zone

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
exps      = ["EXP_020", "EXP_021", "EXP_022", "EXP_023", "EXP_024", "EXP_025"] 

n_exps = len(exps)

labels = ["S2.03",   "S2.05",   "S2.07",   "S2.09",   "S2.11",   "S2.15"]

boundaries= [  [0.01, 0.25, 0.50,                                                                          99.0], \
               [0.01, 0.25, 0.50, 0.75, 1.00,                                                              99.0], \
               [0.01, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00,                                                  99.0], \
               [0.01, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00,                                      99.0], \
               [0.01, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00, 8.00,                          99.0], \
               [0.01, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00, 8.00, 11.00, 14.0, 17.0, 20.0, 99.0], \
            ]

binwidths = [[b[j +  1] - b[j] for j in range(len(b) - 1)] for b in boundaries]

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

# Read thermodynamic mask (based on script fig4.py)
thermomaskfile = repo + "/" + "thermomask.nc"
if not os.path.isfile(thermomaskfile):
    sys.exit("Mask file not found, compute it using fig4.py")
f = Dataset(thermomaskfile, mode = "r")
thermomask = f.variables["thermomask"][:]
f.close()

#We define the variable that will have the itds
# since the number of categories varies, we make that 
# using a list

itd = list()
[itd.append(list()) for e in range(n_exps)] # list of n_exps experiments
[[j.append(list()) for m in range(12)] for j in itd] # 12 months
[[[k.append(list()) for r in range(n_regions)] for k in p] for p in itd]


for j_e, e in enumerate(exps):
    print(j_e)
    # 1. Load the data
    for year in years:
        filein = repo + "/" + e + "/" + e + "_1m_" + str(year) + "0101_" + str(year) + "1231_icemoa.nc"
        f = Dataset(filein, mode = "r")
        siconcat = f.variables["siconcat"][:] * 100.0 # to %
        sithicat = f.variables["sithicat"][:]
        f.close()
        _, ncat, _, _ = siconcat.shape

        if year == yearb:
            data_conc = np.empty((n_years * 12, ncat, ny, nx))
            data_conc[:] = np.nan

            data_thic = np.empty((n_years * 12, ncat, ny ,nx))
            data_thic[:] = np.nan

        data_conc[(year - yearb) * 12 : (year - yearb) * 12 + 12, :, :] = siconcat
        data_thic[(year - yearb) * 12 : (year - yearb) * 12 + 12, :, :] = sithicat

    # Compute seasonal cycles
    cycle_conc = np.empty((12, ncat, ny, nx))
    cycle_thic = np.empty((12, ncat, ny, nx))
    cycle_conc[:] = np.nan
    cycle_thic[:] = np.nan

    area = np.empty((12, n_regions, ncat))
    area[:] = np.nan
    for m in range(12):
        cycle_conc[m, :, :, :] = np.mean(data_conc[m::12, :, :], axis = 0)
        cycle_thic[m, :, :, :] = np.mean(data_thic[m::12, :, :], axis = 0)

        for j_r, r in enumerate(regions):
            if r == "Arctic":
                regionmask = (lat > 0.0)
            elif r == "Antarctic":
                regionmask = (lat < 0.0)
            else:
                sys.exit("(fig2) region unknown")

            # Now for each category we compute the area of ice of that category in the zone
            for jcat in range(ncat):
                #Area of ice in that category
                area[m, j_r, jcat] = compute_area(cycle_conc[m, jcat, :, :], cellarea, mask = mask * thermomask * regionmask)

            for jcat in range(ncat):
                itd[j_e][m][j_r].append(area[m, j_r, jcat] / np.sum(area[m, j_r, :]) / binwidths[j_e][jcat] * 100.0) # %/m


# Plots
fig = plt.figure(figsize = (10, 4))

j_plot = 1
for j_r, r in enumerate(regions):
    # Create Basemap
    if r == "Arctic":
        month = 3 - 1 # March, pythonic
        ymax = 80.0
    elif r == "Antarctic":
        month = 9 - 1 # September, pythonic
        ymax = 150.0

    for j_e, e in enumerate(exps):
        plt.subplot(n_regions, n_exps, j_plot)
        for j in range(len(boundaries[j_e]) - 1):
            b1, b2 = np.log(boundaries[j_e][j]), np.log(boundaries[j_e][j + 1])
            plt.fill((b1, b2, b2, b1), (0.0, 0.0, itd[j_e][month][j_r][j], itd[j_e][month][j_r][j]), color = [0.8, 0.8, 0.8])
            plt.plot((b1, b1), (0, 1e9), color = [0.2, 0.2, 0.2], linestyle = ":", linewidth = 0.5)
        plt.ylim(0.0, ymax)
        if j_e == 0:
            plt.ylabel(r + "\ng(h) [%/m]")
        else:
            plt.yticks([], "")
        if j_r == 0:
             plt.xticks([np.log(h) for h in boundaries[j_e][1:]], [""     for  h in boundaries[j_e][1:]], rotation = 90, fontsize = 7)
             plt.title(labels[j_e])
        else:
             plt.xticks([np.log(h) for h in boundaries[j_e][1:]], [str(h) for  h in boundaries[j_e][1:]], rotation = 90, fontsize = 7)

        plt.xlim(np.log(0.1), np.log(8.0))
        #plt.tight_layout()
        j_plot += 1   

plt.text(-20, -70, "Sea ice thickness [m]", fontsize = 14)
plt.tight_layout(pad = 2.2)#, w_pad=1.5, h_pad=1.0)
plt.savefig("./fig8.png", dpi = 300)
plt.close("all")
