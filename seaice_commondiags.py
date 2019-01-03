#!/usr/bin/python
# Common sea ice diags
# Francois Massonnet & Martin Vancoppenolle
#
import numpy as np
import sys
import scipy.stats


def compute_volume(avgthickness, cellarea, mask = 1):
  """ Input: - avgthickness: sea ice or snow volume per unit cell area, in meters
                             numpy array. if 3-D, time is assumed to be 1st
             - cellarea: array of grid cell areas (sq. meters)
             - mask (1 on ocean, 0 on continent)

      Output: Sea ice or snow volume in the region defined by the mask
  """

  import sys
  import numpy as np

  if np.max(mask) != 1.0 or np.min(mask) < 0.0:
    sys.exit("(compute_volume): mask not between 0 and 1")

  if np.max(avgthickness) > 20.0:
    print("(compute_volume): W A R N I N G: large sea ice thickness")
    print("(compute_volume): np.max(avgthickness) = " + str(np.max(avgthickness)))

  if len(avgthickness.shape) == 3:
    nt, ny, nx = avgthickness.shape
    vol = np.asarray([np.sum(avgthickness[jt, :, :] * cellarea * mask) / 1e12 for jt in range(nt)])
  elif len(avgthickness.shape) == 2:
    vol = np.sum(avgthickness * cellarea * mask) / 1e12
  else:
    sys.exit("(compute_volume): avgthickness has not 2 nor 3 dimensions")

  return vol

def compute_extent(concentration, cellarea, threshold = 15.0, mask = 1):
  """ Input: - sea ice concentration in %
               numpy array. if 3-D, time is assumed to be 1st
             - Threshold over which to consider cell as icy
             - cellarea: array of grid cell areas (sq. meters)
             - mask (1 on ocean, 0 on continent)

      Output: Sea ice extent in the region defined by the mask
  """
  import sys
  import numpy as np
  
  if np.max(concentration) < 10.0:
    sys.exit("(compute_extent): concentration seems to not be in percent")

  if len(concentration.shape) == 3:
    nt, ny, nx = concentration.shape
    ext = np.asarray([np.sum( (concentration[jt, :, :] > threshold) * cellarea * mask) / 1e12 for jt in range(nt)])
  elif len(concentration.shape) == 2:
    ext = np.sum( (concentration > threshold) * cellarea * mask) / 1e12
  else:
    sys.exit("(compute_extent): concentration has not 2 nor 3 dimensions")

  return ext
  
def compute_area(concentration, cellarea, mask = 1):
  """ Input: - sea ice concentration in %
               numpy array. if 3-D, time is assumed to be 1st
             - cellarea: array of grid cell areas (sq. meters)
             - mask (1 on ocean, 0 on continent)

      Output: Sea ice area in the region defined by the mask
  """
  import sys
  import numpy as np

  if np.max(concentration) < 10.0:
    sys.exit("(compute_area): concentration seems to not be in percent")

  if len(concentration.shape) == 3:
    nt, ny, nx = concentration.shape
    are = np.asarray([np.sum( concentration[jt, :, :] / 100.0 * cellarea * mask) / 1e12 for jt in range(nt)])
  elif len(concentration.shape) == 2:
    are = np.sum( concentration / 100.0 * cellarea * mask) / 1e12
  else:
    sys.exit("(compute_area): concentration has not 2 nor 3 dimensions")

  return are

def mask_ice(concentration, threshold = 15.0):
   """ Input  - sea ice concentration in fractional units: time [optional], y, x
       Output - mask: 1 if concentration reached threshold or more at least once
   """
   import numpy as np
   import sys

   if np.max(concentration) < 10.0:
    sys.exit("(mask_ice): concentration seems to not be in percent")

   if len(concentration.shape) == 2:
     mask = 1.0 * (concentration > threshold)
   elif len(concentration.shape) == 3:
     mask = np.max(1.0 * (concentration > threshold), axis = 0)
   else:
     sys.exit("(mask_ice): input concentration has incorrect dimensions")

   return mask
