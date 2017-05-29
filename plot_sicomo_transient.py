# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
#from helper_functions import decorate_time_axis_yearmeans
from scipy.io import netcdf
from custom_io import get_remote_data

def load(f):
    prepath = "pgierz@stan1:/ace/user/pgierz/cosmos-aso-wiso/LIG-Tx10/pre/mpiom/"+f
    return netcdf.netcdf_file(get_remote_data(prepath))

def decorate_time_axis_yearmeans(ax, suppress_ticks=False, shading=0.4):
    """This function helps to get the time axis of a timeseries for the
    transient run looking pretty. You have the option to suppress the
    ticks with a boolean, useful if for example you are making a
    multi-variable (stacked) timeseries plot.

    Paul Gierz, 2016
    """
    # Assume we have year means with the spinup period from the
    # LIG-Tx10 run. We then have 200 years of spinup and 1500 years of
    # actual simulation.
    # Get the x and y limits:
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    ax.fill_between(np.arange(1500, 1700), *ylims, color="gray", alpha=shading, hatch="//")
    tick_locations = np.arange(0, 200 + 1500 + 100, 100)
    tick_labels = ["Period", "Spinup", "130", "129", "128", "127", "126", "125", "124", "123", "122", "121", "120", "119", "118", "117", "116", "115"]
    tick_labels.reverse()
    if not suppress_ticks:
        ax.set_xticks(tick_locations)
        ax.set_xticklabels(tick_labels)
    else:
        ax.set_xticks(tick_locations)
        ax.set_xticklabels([])
    ax.set_xlabel("Time (ka BP)")

f, ax = plt.subplots(1, 1, figsize=(10, 4))

fin1 = load("LIG-Tx10_mpiom_SICOMO_remap_32_172_September_runmin100_runmean30.nc")
fin2 = load("LIG-Tx10_mpiom_SICOMO_remap_32_172_September_runmean30.nc")
fin3 = load("LIG-Tx10_mpiom_SICOMO_remap_32_172_September.nc")

fin4 = load("LIG-Tx10_mpiom_SICOMO_remap_32_170_September_runmin100_runmean30.nc")
fin5 = load("LIG-Tx10_mpiom_SICOMO_remap_32_170_September_runmean30.nc")
fin6 = load("LIG-Tx10_mpiom_SICOMO_remap_32_170_September.nc")

decorate_time_axis_yearmeans(ax)
plt.plot(fin3.variables["SICOMO"].data.squeeze()[::-1], lw=0.5, color="gray", alpha=0.2)
plt.plot(fin1.variables["SICOMO"].data.squeeze()[::-1], lw=2, color="black")
plt.plot(fin2.variables["SICOMO"].data.squeeze()[::-1], lw=2, color="black")

plt.plot(fin6.variables["SICOMO"].data.squeeze()[::-1], lw=0.5, color="orange", alpha=0.2)
plt.plot(fin4.variables["SICOMO"].data.squeeze()[::-1], lw=2, color="red")
plt.plot(fin5.variables["SICOMO"].data.squeeze()[::-1], lw=2, color="red")

plt.ylabel("Simulated \n Sea Ice Concentration")
plt.xlim(0, 1700)
plt.ylim(0.0, 1.0)
plt.show()
#plt.savefig("Transient_Seaice.png") 
#print "Done!"
exit

