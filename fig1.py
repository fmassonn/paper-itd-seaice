#!/usr/bin/python
#
# Author - Francois Massonnet
# Date - Jan 3, 2019

# Plots Fig. 1 of the paper: category limits of ITD
import matplotlib.pyplot as plt
import numpy as np
import sys

exec(open("./namelist.py"))

# First set of experiments: standard ITD of LIM
# ---------------------------------------------    

table = [[m[0], m[3], m[2]] for m in metadata if m[0][0:2] == "S1"]
fig = plt.figure(figsize = (4, 7))

plt.subplot(3, 1, 1)

xl = 0.0
xu = 6.5
for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0


    plt.plot((xl, xu), (yl, yl), color = table[j][2])
    plt.plot((xl, xu), (yu, yu), color = table[j][2])
    plt.plot((xl, xl), (yl, yu), color = table[j][2])
    [plt.plot((x, x), (yl, yu), color = table[j][2]) for x in table[j][1]]

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.xlabel("Ice thickness [m]")
plt.xlim(-xu / 30.0, xu)
plt.yticks(np.arange(len(table) + 1, 1, -1), [t[0] for t in table])
plt.tight_layout()

# Second set of experiments: prescribed ITD by appending
# ------------------------------------------------------    
table = [[m[0], m[3], m[2]] for m in metadata if m[0][0:2] == "S2"]

plt.subplot(3, 1, 2)

xl = 0.0
xu = 24.0
for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0


    plt.plot((xl, xu), (yl, yl), color = table[j][2])
    plt.plot((xl, xu), (yu, yu), color = table[j][2])
    plt.plot((xl, xl), (yl, yu), color = table[j][2])
    [plt.plot((x, x), (yl, yu), color =  table[j][2]) for x in table[j][1]]

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.xlabel("Ice thickness [m]")
plt.xlim(-xu / 30.0, xu)
plt.yticks(np.arange(len(table) + 1, 1, -1), [t[0] for t in table])
plt.tight_layout()

# Third set of experiments: prescribed ITD by refining or collapsing S2
# ---------------------------------------------------------------------
table = [[metadata[j][0], metadata[j][3], metadata[j][2]] for j in [14, 13, 9, 12]]

plt.subplot(3, 1, 3)

xl = 0.0
xu = 4.5
for j in range(len(table)):
    yu = len(table) - j + 1 + 1.0 / 3.0
    yl = len(table) - j + 1 - 1.0 / 3.0


    plt.plot((xl, xu), (yl, yl), color = table[j][2])
    plt.plot((xl, xu), (yu, yu), color = table[j][2])
    plt.plot((xl, xl), (yl, yu), color = table[j][2])
    [plt.plot((x, x), (yl, yu), color = table[j][2]) for x in table[j][1]]

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().set_aspect(aspect = 0.4)
plt.xlabel("Ice thickness [m]")
plt.xlim(-xu / 30.0, xu)
plt.yticks(np.arange(len(table) + 1, 1, -1), [t[0] for t in table])
plt.tight_layout()
plt.savefig("./fig1.pdf", dpi = 300)

