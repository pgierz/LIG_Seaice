#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from plot_tools import _decorate_x_axes_for_ymonmean
from simulation_tools import cosmos_standard_analysis
import cdo
from custom_io import get_remote_data
from scipy.io import netcdf


CDO = cdo.Cdo(cdfMod = "scipy")

user="pgierz"
host="stan1"
prepath = "pgierz@stan1:/ace/user/pgierz/cosmos-aso-wiso"
Eem130 = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "Eem130-S2").ymonmean("SICOMO")
PI = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "EXP003").ymonmean("SICOMO")

# Runs with altered Berring Straight
prepath = "pgierz@stan1:/ace/user/pgierz/cosmos-aso"
Sensitivity_130 = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "LIG130_dles_nbs_w").ymonmean("SICOMO")

f, axs = plt.subplots(2, 2)
lons = [30.983333333333334, 140.06666666666666, 171.71666666666667, 14.033333333333333]
lats = [81.9, 81.31666666666666, 85.23333333333333, 85.55]
titles = ["PS2138-2", "PS2757-8", "PS51/38-3", "PS2200-2"]

for ax, lon, lat, tit in zip(axs.flatten(), lons, lats, titles):
    E130 = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=Eem130.filename, returnArray="SICOMO").squeeze()
    Sens = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=Sensitivity_130.filename, returnArray="SICOMO").squeeze()
    CTRL = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=PI.filename, returnArray="SICOMO").squeeze()

    ax.plot(E130, "o-", label="LIG-130")
    ax.plot(Sens, "o-", label="LIG-130 Sensitivity Test")
    ax.plot(CTRL, "o-", label="PI", color="black")
    ax.set_title(tit)
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("Sea Ice Concentration (-)")
    _decorate_x_axes_for_ymonmean(ax)

plt.subplots_adjust(bottom=0.2)
plt.legend(loc=0, ncol=3, bbox_to_anchor=(0.2, -0.2))
# f.setSubplotParams(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
# plt.savefig("Seaice_seasonal_cycle_RStein.png")
# plt.close()
plt.show()
exit
