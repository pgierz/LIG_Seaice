#!/bin/env python

import tarfile
import matplotlib.pyplot as plt
import os
import cdo
import glob
import numpy as np
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from basemap_wrappers.basemap_nhem import map_nhem
from plot_tools import plot_var_from_ncdf_file
from scipy.io import netcdf

CDO = cdo.Cdo(cdfMod="scipy")
seaice_array_mean = np.array([])
seaice_array_max = np.array([])
seaice_array_min = np.array([])


expid="LIG130_dles_nbs_w"
path="/ace/user/pgierz/cosmos-aso/"

if not os.path.exists('timeser_dir'): os.mkdir('timeser_dir')

for fin in glob.glob(path+expid+"/outdata/mpiom/*.tar"):
    f = tarfile.open(fin)
    timeser_name = f.name.split("/")[-1].replace("fort_", "TIMESER.").replace("tar", "ext")
    f.extract(timeser_name, 'timeser_dir')
    fout_mean = CDO.yearmean(input="timeser_dir/"+timeser_name,
                        options="-f nc",
                        returnArray="var56").squeeze()

    fout_max = CDO.yearmax(input="timeser_dir/"+timeser_name,
                        options="-f nc",
                        returnArray="var56").squeeze()

    fout_min = CDO.yearmin(input="timeser_dir/"+timeser_name,
                        options="-f nc",
                        returnArray="var56").squeeze()

    seaice_array_mean = np.append(seaice_array_mean, fout_mean)
    seaice_array_max = np.append(seaice_array_max, fout_max)
    seaice_array_min = np.append(seaice_array_min, fout_min)

fig, ax1 = plt.subplots()
ax1.plot(seaice_array_mean, color="black", lw=2)
ax1.plot(seaice_array_min, color="gray", lw=0.5)
ax1.plot(seaice_array_max, color="gray", lw=0.5)
ax1.set_xlabel("Simulation Time (years)")
ax1.set_ylabel("Sea Ice Area Arctic Basin (m$^{2}$)")

# Add a subplot to show the Arctic basin averaging area
ax2 = inset_axes(ax1, width="30%", height="30%", loc=4)
m = map_nhem(fill_color=None, thisax=ax2)
bek_file = netcdf.netcdf_file("/home/ace/pgierz/reference_stuff/bek_2.nc")
plot_var_from_ncdf_file("THO", bek_file, m)
plt.show()
