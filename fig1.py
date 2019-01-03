#!/usr/bin/python
#
# Author - Francois Massonnet
# Date - Jan 3, 2019

# Plots Fig. 1 of the paper: category limits of ITD
import matplotlib.pyplot as plt
import numpy as np
import sys

def LIM_itd(N, hbar = 2.0, alpha = 0.05):
    """
    Function returning the category limits for the LIM3 formulation

    N    : number of categories
    hbar : expected mean thickness over the domain
    alpha: exponent controlling the shape of the ITD

    Returns: the N upper limits of the N categories
    """

    if (type(N) is not int) or (N < 1):
        sys.exit("(f) error: N not valid")
  

    def fun(i):
        return ((N * (3.0 * hbar + 1.0) ** alpha) / \
               ((N - i) * (3.0 * hbar + 1.0) ** alpha + i) ) ** (alpha ** (-1.0)) \
               - 1.0

    out = [fun(i) for i in range(1, N + 1)]
    out[-1] = 99.0 # LIM convention to replace last boundary
    
    return out


table = [\
         ["S1.50", LIM_itd(50)], \
         ["S1.30", LIM_itd(30)], \
         ["S1.10", LIM_itd(10)], \
         ["S1.05", LIM_itd(5 )], \
         ["S1.03", LIM_itd(3 )], \
         ["S1.01", LIM_itd(1 )], \
        ]

fig = plt.figure(figsize = (6, 3))

plt.subplot(3, 1, 1)

for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0
    xl = 0.0
    xu = 6.5

    plt.plot((xl, xu), (yl, yl), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xu), (yu, yu), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xl), (yl, yu), color = [0.2, 0.2, 0.2])

plt.savefig("./fig1.png", dpi = 300)

