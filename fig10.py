#!/usr/bin/python
#
# Author Francois Massonnet
# Date January 2019
import numpy as np
import matplotlib.pyplot as plt

# Plot performance as function of number of categories

n_cat = [5, 1, 3, 10, 30, 50, 3, 5, 7, 9, 11, 15, 5, 17, 33]
n_exp = len(n_cat)

time = np.array([
    [30.50, 30.75, 30.66, 31.00, 30.75] , \
    [29.00, 29.30, 29.60, 29.60, 30.00] , \
    [30.50, 30.40, 30.45, 30.85, 30.25] , \
    [35.50, 35.30, 37.40, 36.00, 37.40] , \
    [59.75, 59.75, 60.50, 60.25, 61.00] , \
    [83.25, 86.00, 85.25, 85.75, 85.20] , \
    [30.10, 30.00, 29.85, 29.85, 30.25] , \
    [31.50, 31.60, 31.50, 31.60, 30.85] , \
    [32.40, 32.50, 32.40, 32.45, 32.10] , \
    [34.85, 34.60, 34.50, 34.10, 34.15] , \
    [36.00, 36.45, 36.50, 36.45, 36.50] , \
    [39.75, 39.90, 39.80, 40.00, 39.90] , \
    [29.75, 30.66, 30.25, 30.40, 30.25] , \
    [40.40, 41.75, 41.75, 42.00, 43.50] , \
    [61.90, 61.66, 61.40, 63.00, 61.40] , \
    ]) 

ave_time = np.mean(time, 1) ;
plt.figure(figsize = (4, 3))

for j_exp in np.arange(n_exp):
    plt.scatter(n_cat[j_exp], ave_time[j_exp], 50, marker = "x", color = [0.2, 0.2, 0.2])


plt.xlim(0, 52)
plt.ylim(0, 90)
plt.xlabel("Number of categories") ;
plt.ylabel("Wall-clock time per year\nof simulation [min]")
plt.grid()
plt.gca().set_axisbelow(True)
plt.tight_layout()
plt.savefig("./fig10.png", dpi = 300) ;

