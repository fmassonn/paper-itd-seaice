# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:51:56 2019

@author: massonnetf
"""

# Plots Fig. 1 of the paper: category limits of ITD
import matplotlib.pyplot as plt
import numpy as np
import sys

if sys.version_info.major == 3:
    exec(open("./namelist.py").read())
k = 2.0 
dT = 30.0 
Lf = 334000
rho = 917.0

q = list()
cats = range(1, 31)#[1, 3, 5, 10, 20, 30, 50, 100]
for ncat in cats:
    print(ncat)
    
    plt.figure("fig", figsize = (4, 3))
    itd_bounds = np.concatenate(([0.0], LIM_itd(ncat)))
    itd_bounds[-1] = 10.0
 
    mu = 3.0 # mean thickness
    st = 2.0 # standard deviation
    
    # Log-normal that has these moments
    m = np.log(mu ** 2 / np.sqrt(mu ** 2 + st ** 2))
    s = np.sqrt(np.log((mu ** 2 + st ** 2) / mu ** 2))
    
    
    
    def g(h):
        return 1.0 / (h * np.sqrt(2 * np.pi * s ** 2)) * np.exp(- (np.log(h) - m) ** 2 / (2 * s **2))
    
    nc = len(itd_bounds)
    
    h = np.linspace(0.1, 100, 1000)
    
    plt.plot(h, 100 * g(h), color = [0.5, 0.0, 0.0], lw = 3, label = "Supposed distribution")
    
    for jnc in range(nc - 1):
        midpoint = (itd_bounds[jnc] + itd_bounds[jnc + 1]) / 2
        width = itd_bounds[jnc + 1] - itd_bounds[jnc]
        if jnc == 0:
            lab = "ITD discretization"
        else:
            lab = None
        plt.bar(midpoint, 100 * g(midpoint) , width = width, color = "grey", edgecolor = "black", label = lab)
        
        if ncat == 5:
            if jnc == 0:
                lab2 = "Supposed distribution"
            else:
                lab2 = None
            plt.figure("fig2", figsize = (8, 3))
            plt.subplot(1, 2, 1)
            plt.plot(h, 100 * g(h), color = [0.5, 0.0, 0.0], lw = 3, label = lab2)
            plt.bar(midpoint, 100 * g(midpoint) , width = width, color = "grey", edgecolor = "black", label = lab)
            plt.ylabel("g(h) [%/m]")
            plt.xlabel("h [m]")
            plt.legend()
            plt.grid()
            plt.xlim(0.0, 15.0)

      
    plt.figure("fig", figsize = (4, 3))
    
    plt.ylabel("g(h) [%/m]")
    plt.xlabel("h [m]")
    plt.legend()
    plt.xlim(0.0, 15.0)
    
    # Average heat conduction flux, supposing h = average
    hav = (itd_bounds[:-1] + itd_bounds[1:]) / 2
    dh =  (itd_bounds[1:] - itd_bounds[:-1])
    qav = np.sum(k * dT / hav * g(hav) * dh)
    gr  = qav / (rho * Lf) * 86400.0 * 1000.0
    q.append(gr)
    plt.title(str(ncat) + " categories: growth rate = " + str(np.round(gr, 1)) + " mm/day")
    plt.grid()
    plt.tight_layout()
    plt.savefig(str(ncat).zfill(4) + ".png", dpi = 600)
    plt.close("fig")
    
    

plt.figure("fig2")
plt.subplot(1, 2, 2)
plt.plot(cats, q, "k.-", lw = 2)
plt.ylabel("Average growth\nrate [mm/day]")
plt.xlabel("Number of ice thickness categories")
plt.title("Theoretical growth rate")
plt.grid()
plt.tight_layout()
plt.savefig("./figS6.png", dpi = 600)
plt.savefig("./figS6.pdf", dpi = 600)


    
