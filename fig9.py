#!/usr/bin/python

# Author Francois Massonnet
# Date Jan 2019

# Figure 7 of the ITD paper: seasonal cycles of sea ice extent and volume

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
indices = [12, 9, 13, 14, 15]

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


diags = ["volume"]
units = ["10$^3$ km$^3$"]
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
                    volshort  = "PIOMAS"
                elif r == "Antarctic":
                    shortname = "sh"
                    volshort = "GIOMAS"
                else: 
                    sys.exit("(fig2) region unknown")

                if d == "extent":
                    filein = repo + "/REF/" + "siconc_SImon_OSI-409a_r1i1p1_197901-201512_" + shortname + ".nc"
                    f = Dataset(filein, mode = "r")
                    siconc = f.variables["siconc"][:]
                    mask_or= f.variables["sftof"][:]
                    cellarea_or=f.variables["areacello"][:]
                    latitude_or=f.variables["latitude"][:]
                    f.close()
                    if r == "Arctic":
                        regionmask = (latitude_or > 0.0)
                    elif r == "Antarctic":
                        regionmask = (latitude_or < 0.0)
                    else:
                        sys.exit("(fig2) region unknown")
                    diag =  compute_extent(siconc, cellarea_or, threshold = 15.0, mask = mask_or * regionmask)
                    data[j_d, j_r, j_e, :] = diag[(yearb - 1979) * 12:(yeare - 1979) * 12 + 12]


                if d == "volume":
                    filein = repo + "/REF/" + "sivol_SImon_" + volshort + "_r1i1p1_197901-201512.nc"
                    f = Dataset(filein, mode = "r")
                    sivol = f.variables["sivol"][:]
                    mask_or=f.variables["sftof"][:]
                    cellarea_or=f.variables["areacello"][:]
                    latitude_or = f.variables["latitude"][:]
                    f.close()
                    if r == "Arctic":
                        regionmask = (latitude_or > 0.0)
                    elif r == "Antarctic":
                        regionmask = (latitude_or < 0.0)
                    else:
                        sys.exit("(fig2) region unknown")

                    diag = compute_volume(sivol, cellarea_or, mask = mask_or * regionmask)
                    data[j_d, j_r, j_e, :] = diag[(yearb - 1979) * 12:(yeare - 1979) * 12 + 12]
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
fig = plt.figure(figsize = (5, 8))

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
            plt.scatter(newtime, newseries, 80, marker = "*", color = colors[j_e], zorder = 1000, edgecolor = "white", linewidth = 0.2)

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
   
        plt.gca().yaxis.grid(True)
        j_plot += 1

plt.tight_layout()
plt.savefig("./fig9.pdf", dpi = 300)
plt.close("all")
