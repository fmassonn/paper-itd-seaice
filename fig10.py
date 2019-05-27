#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 10 of the ITD paper: seasonal cycles mass balance


import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import interp1d
import os

# Import functions
from seaice_commondiags import *

# Import directory location
exec(open("namelist.py"))

# Years
yearb, yeare = 1995, 2014
years = np.arange(yearb, yeare + 1)
n_years = len(years)

# indices of experiments to plot (from namelist)
indices = [0, 2, 5]#, 8, 9, 5]

# Experiments to plot
exps   = [metadata[i][1] for i in indices]
n_exps = len(exps)

labels = [metadata[i][0] for i in indices]
colors = [metadata[i][2] for i in indices]

# Read NEMO grid
gridfile = repo + "/" + "mesh_mask_nemo.N3.6_ORCA1L75.nc"
f = Dataset(gridfile, mode = "r")
e1t = f.variables["e1t"][0, :, :]
e2t = f.variables["e2t"][0, :, :]
cellarea = e1t * e2t
lat = f.variables["gphit"][0, :, :]
lon = f.variables["glamt"][0, :, :]
mask= f.variables["tmaskutil"][0, :, :]
f.close()

# Read thermodynamic mask (based on script fig4.py)
thermomaskfile = repo + "/" + "thermomask.nc"
if not os.path.isfile(thermomaskfile):
    sys.exit("Mask file not found, compute it using fig4.py")
f = Dataset(thermomaskfile, mode = "r")
thermomask = f.variables["thermomask"][:]
f.close()

regions =   ["Arctic", "Antarctic"]
n_regions = len(regions)

diags = ["vfxbog", "vfxsni", "vfxdyn",    # Ice production: bottom growth, snow-ice and dynamic 
         "vfxsum", "vfxbom"]    # Ice melt      : surface and bottom
                                # All in m/day
diags_long = ["Basal growth", "Snow-ice production", "Dynamic production",
              "Surface melt", "Bottom melt"]

cols  = [[0.0, 0.0, 0.3], [0.4, 0.4, 1.0], [0.8, 0.8, 1.0],
         [0.5, 0.0, 0.0], [1.0, 0.5, 0.5]]
n_diags = len(diags)

data = np.empty((n_diags, n_regions, n_exps, n_years * 12))
data[:] = np.nan

# Seasonal cycles
cycles = np.empty((n_diags, n_regions, n_exps, 12))
cycles[:] = np.nan

# Seasonal means
smeans = np.empty((n_diags, n_regions, n_exps, 4))
smeans[:] = np.nan

for j_e, e in enumerate(exps):
    print(e)
    # 1. Load the data
    for year in years:
        filein = repo + "/" + e + "/" + e + "_1m_" + str(year) + "0101_" + str(year) + "1231_icemod.nc"
        f = Dataset(filein, mode = "r")
	for j_d, d in enumerate(diags):
            myvar = f.variables[diags[j_d]][:] * 1000.0 # m/day to mm / day
 
            # Compute diagnostics
            for j_r, r in enumerate(regions):
                if r == "Arctic":
                    maskregion = (lat > 0.0) * thermomask * mask
                elif r == "Antarctic":
                    maskregion = (lat < 0.0) * thermomask * mask
                else:
                    sys.exit("(fig10) region unknown")

                # Minus sign to have growth positive, melt negative
                diag = np.asarray([-np.sum( myvar[jt, :, :] * cellarea * maskregion) / np.sum(cellarea * maskregion) for jt in range(myvar.shape[0])])
                data[j_d, j_r, j_e, (year - yearb) * 12 : (year - yearb) * 12 + 12] = diag
    
        f.close()

    # 2. Compute seasonal cycles
    for j_d, d in enumerate(diags):
        for j_r, r in enumerate(regions):
            series = data[j_d, j_r, j_e, :]  
            cycles[j_d, j_r, j_e, :] = np.array([np.mean(series[m::12]) for m in np.arange(12)])
            smeans[j_d, j_r, j_e, :] = np.array([np.mean(cycles[j_d, j_r, j_e, jm:jm + 3]) for jm in [0, 3, 6, 9]])

# Plots
fig = plt.figure(figsize = (6, 7))

j_plot = 1
#
for j_r, r in enumerate(regions):
    plt.subplot(n_regions, 1, j_plot)
    for j_e, e in enumerate(exps):
        # Bar plot the mass balance terms
        for j_d, d in enumerate(diags):
            x = np.arange(smeans.shape[-1])
            w = 1.0 / (n_exps + 1) 
            if j_e == 0: #Legend only once
                legend = diags_long[j_d]
            else:
                legend = None

            ## Plot total for dynamic and bottom melt contributions (graphical twist)
            #if d == "vfxdyn":
            #    find_j_d1 = diags.index("vfxbog")
            #    find_j_d2 = diags.index("vfxsni")
            #    height = smeans[j_d, j_r, j_e, :] + smeans[find_j_d1, j_r, j_e, :] + smeans[find_j_d2, j_r, j_e, :]
            #    zorder = 0
            #if d == "vfxsni":
            #    # Find index of other contribution
            #    find_j_d = diags.index("vfxbog")
            #    height = smeans[j_d, j_r, j_e, :] + smeans[find_j_d, j_r, j_e, :]
            #    zorder = 100
            #elif d == "vfxbom":
            #    find_j_d = diags.index("vfxsum")
            #    height =  smeans[j_d, j_r, j_e, :] + smeans[find_j_d, j_r, j_e, :]
            #    zorder = 1
            #else:
            #    height = smeans[j_d, j_r, j_e, :]
            #    zorder = 1000

            #if j_r == 0 and j_e == 0:
            #  print(d)
            #  print(height[0])
            if j_d == 0 or j_d == 3:
                bottom = 0.0
            elif j_d < 3:
                bottom = np.sum(smeans[0:j_d, j_r, j_e, :], axis = 0)
            else:
                bottom = np.sum(smeans[3:j_d, j_r, j_e, :], axis = 0) #+ smeans[j_d, j_r, j_e, :]

            height = smeans[j_d, j_r, j_e, :]                     
  
            plt.bar(x + 1.0 * j_e / (n_exps + 1), height = height, width = w * 0.9, \
                    color = cols[j_d], align = "edge", label = legend, \
                    bottom = bottom)

        # Plot net term (only after last diag)
        for jm in range(smeans.shape[-1]):
            if j_e == 0 and jm == 0:
                legend = "Net"
            else: 
                legend = None

            net = np.sum(smeans[:, j_r, j_e, jm])
            x = jm    
            plt.plot((x + 1.0 * j_e / (n_exps + 1), x + 1.0 * j_e / (n_exps + 1) + 0.9 * w), (net, net),
                  label = legend, color =  "lightgreen", linestyle = ":", zorder = 2000)


        plt.title(r + " sea ice mass balance")
        plt.xlim(-0.5, 4.5)
        plt.plot((-0.5, 4.5), (0.0, 0.0), "k", zorder = 10000)
        plt.ylim(-12, 12)
        plt.xticks([n + 0.5 * w * n_exps for n in range(4)], ["Jan-Feb-Mar", "Apr-May-Jun", "Jul-Aug-Sep", "Oct-Nov-Dec"])
        plt.ylabel("mm/day")
        plt.legend(fontsize = 8)
    plt.grid()
    plt.gca().xaxis.grid(False)

    j_plot += 1
        #plt.gca().xaxis.grid(False)
plt.tight_layout()
plt.savefig("./fig10.pdf", dpi = 300)
plt.savefig("./fig10.png", dpi = 600)
plt.close("all")
