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



# First set of experiments: standard ITD of LIM
# ---------------------------------------------    
table = [\
         ["S1.50", LIM_itd(50)], \
         ["S1.30", LIM_itd(30)], \
         ["S1.10", LIM_itd(10)], \
         ["S1.05", LIM_itd(5 )], \
         ["S1.03", LIM_itd(3 )], \
         ["S1.01", LIM_itd(1 )], \
        ]

fig = plt.figure(figsize = (6, 10))

plt.subplot(3, 1, 1)

xl = 0.0
xu = 6.5
for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0


    plt.plot((xl, xu), (yl, yl), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xu), (yu, yu), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xl), (yl, yu), color = [0.2, 0.2, 0.2])
    [plt.plot((x, x), (yl, yu), color = [0.2, 0.2, 0.2]) for x in table[j][1]]

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.xlabel("Ice thickness [m]")
plt.xlim(-xu / 30.0, xu)
plt.yticks(np.arange(len(table) + 1, 1, -1), [t[0] for t in table])
plt.tight_layout()

# Second set of experiments: prescribed ITD by appending
# ------------------------------------------------------    
table = [\
         ["S2.15", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00, 8.00, 11.00, 14.0, 17.0, 20.0, 99.0]], \
         ["S2.11", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00, 8.00,                          99.0]], \
         ["S2.09", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00,                                      99.0]], \
         ["S2.07", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00,                                                  99.0]], \
         ["S2.05", [0.25, 0.50, 0.75, 1.00,                                                              99.0]], \
         ["S2.03", [0.25, 0.50,                                                                          99.0]], \
        ]

plt.subplot(3, 1, 2)

xl = 0.0
xu = 24.0
for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0


    plt.plot((xl, xu), (yl, yl), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xu), (yu, yu), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xl), (yl, yu), color = [0.2, 0.2, 0.2])
    [plt.plot((x, x), (yl, yu), color = [0.2, 0.2, 0.2]) for x in table[j][1]]

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.xlabel("Ice thickness [m]")
plt.xlim(-xu / 30.0, xu)
plt.yticks(np.arange(len(table) + 1, 1, -1), [t[0] for t in table])
plt.tight_layout()

# Third set of experiments: prescribed ITD by refining or collapsing S2
# ---------------------------------------------------------------------
table = [\
         ["S3.33", [0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.50, 0.5625, 0.625, 0.6875, 0.75, 0.8125, 0.875, 0.9375, 1.00, 1.125, 1.25, 1.375, 1.50, 1.625, 1.75, 1.875, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 99.0]], \
         ["S3.17", [        0.125,         0.25,         0.375,         0.50,         0.625,         0.75,         0.875,         1.00,        1.25,        1.50,        1.75,        2.00,       2.50,       3.00,       3.50,       4.00, 99.0]], \
         ["S2.09", [                       0.25,                        0.50,                        0.75,                        1.00,                     1.50,                     2.00,                   3.00,                   4.00, 99.0]], \
         ["S3.05", [                                                    0.50,                                                     1.00,                                               2.00,                                           4.00, 99.0]], \
        ]

plt.subplot(3, 1, 3)

xl = 0.0
xu = 4.5
for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0


    plt.plot((xl, xu), (yl, yl), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xu), (yu, yu), color = [0.2, 0.2, 0.2])
    plt.plot((xl, xl), (yl, yu), color = [0.2, 0.2, 0.2])
    [plt.plot((x, x), (yl, yu), color = [0.2, 0.2, 0.2]) for x in table[j][1]]

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().set_aspect(aspect = 0.4)
plt.xlabel("Ice thickness [m]")
plt.xlim(-xu / 30.0, xu)
plt.yticks(np.arange(len(table) + 1, 1, -1), [t[0] for t in table])
plt.tight_layout()
plt.savefig("./fig1.png", dpi = 300)

