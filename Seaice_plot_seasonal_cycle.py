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
Eem125 = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "Eem125-S2").ymonmean("SICOMO")
Eem120 = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "Eem120-S2").ymonmean("SICOMO")
PI = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "EXP003").ymonmean("SICOMO")

# Runs with future CO2
prepath = "pgierz@stan1:/ace/user/pgierz/cosmos-ao"
RCP6 = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "r6ao").ymonmean("SICOMO")
RCP4 = cosmos_standard_analysis(user, host, prepath.split(":")[-1], "r4ao").ymonmean("SICOMO")
RCP4_early = netcdf.netcdf_file(get_remote_data(prepath+"/r4ao/post/mpiom/r4ao_mpiom_SICOMO_2070-2100_ymonmean_remap.nc"))
RCP6_early = netcdf.netcdf_file(get_remote_data(prepath+"/r6ao/post/mpiom/r6ao_mpiom_SICOMO_2070-2100_ymonmean_remap.nc"))


# Reduced GRIS
GRIS = cosmos_standard_analysis("pgierz", "rayl4", "/csys/nobackup1_PALEO/pgierz/cosmos-aso/", "pfe0021").ymonmean("SICOMO")

f, axs = plt.subplots(2, 2)
lons = [30.983333333333334, 140.06666666666666, 171.71666666666667, 14.033333333333333]
lats = [81.9, 81.31666666666666, 85.23333333333333, 85.55]
titles = ["PS2138-2", "PS2757-8", "PS51/38-3", "PS2200-2"]

for ax, lon, lat, tit in zip(axs.flatten(), lons, lats, titles):
    E130 = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=Eem130.filename, returnArray="SICOMO").squeeze()
    E125 = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=Eem125.filename, returnArray="SICOMO").squeeze()
    E120 = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=Eem120.filename, returnArray="SICOMO").squeeze()
    R4 = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=RCP4.filename, returnArray="SICOMO").squeeze()
    R4e = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=RCP4_early.filename, returnArray="var15").squeeze()
    R6 = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=RCP6.filename, returnArray="SICOMO").squeeze()
    R6e = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=RCP6_early.filename, returnArray="var15").squeeze()
    G = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=GRIS.filename, returnArray="SICOMO").squeeze()
    CTRL = CDO.remapnn("lon="+str(lon)+"/lat="+str(lat), input=PI.filename, returnArray="SICOMO").squeeze()

    ax.plot(E130, "o-", label="LIG-130")
    ax.plot(E125, "o-", label="LIG-125")
    ax.plot(E120, "o-", label="LIG-120")
    ax.plot(G, "o-", label="LIG-130, Reduced GrIS")
    ax.plot(R4, "o:", color="purple", label="RCP4.5 (2300)") 
    ax.plot(R4e, "o-", color="purple", label="RCP4.5 (2100)")
    ax.plot(R6, "o:", color="pink", label="RCP6 (2300)")
    ax.plot(R6e, "o-", color="pink", label="RCP6 (2100)")
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
