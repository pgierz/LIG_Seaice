#!/usr/bin/env python
import matplotlib.pyplot as plt
from basemap_wrappers.basemap_nhem import map_nhem
#from custom_io.get_remote_data import get_remote_data
from plot_tools import plot_var_from_ncdf_file_timestep
import numpy as np

from simulation_tools import cosmos_standard_analysis
from plot_tools import plot_overturning_contours, plot_overturning_anom_contours

exps = [line.strip() for line in open("/Users/pgierz/Research/Eem_Hol_Wiso/exps.dat", 'r') if "#" not in line]
expids = [e.split("/")[-1] for e in exps]

user="pgierz"
host="stan1"
path="/ace/user/pgierz/cosmos-aso-wiso/"

def import_required_data_seaice_concentration():
    return {eid: cosmos_standard_analysis(user, host, path, eid).ymonmean("SICOMO") for eid in expids}


amoc_dict = {eid: cosmos_standard_analysis(user, host, path, eid).AMOC_spatial_timmean() for eid in expids}

contourf_opts = {
    "cmap": plt.cm.jet,
    "levels": np.arange(0, 1.05, 0.05)
}

amoc_anom_opts = {
    "cmap": plt.cm.PuOr,
    "levels": np.arange(-4.0, 5, 1)
}

amoc_abs_opts = {
    "cmap": plt.cm.jet,
    "levels": np.arange(-4.0, 20, 2)
}

if __name__ == '__main__':
    sim_dict = import_required_data_seaice_concentration()
    
    f, axs = plt.subplots(4, 4)

    # Set Titles
    axs[0, 0].set_title("LIG-130")
    axs[0, 1].set_title("LIG-125")
    axs[0, 2].set_title("LIG-120")
    axs[0, 3].set_title("PI")

    # Set Month Labels
    axs[0, 0].set_ylabel("March")  # 2
    axs[1, 0].set_ylabel("June")  # 5
    axs[2, 0].set_ylabel("September")  # 8
    
    for ax, eid in zip(axs[0, :], expids):
        m = map_nhem(thisax=ax, fill_color=None, coastlines=False)
        plot_var_from_ncdf_file_timestep("SICOMO", 2, sim_dict[eid], m, **contourf_opts)

    for ax, eid in zip(axs[1, :], expids):
        m = map_nhem(thisax=ax, fill_color=None, coastlines=False)
        plot_var_from_ncdf_file_timestep("SICOMO", 5, sim_dict[eid], m, **contourf_opts)

    for ax, eid in zip(axs[2, :], expids):
        m = map_nhem(thisax=ax, fill_color=None, coastlines=False)
        p1 = plot_var_from_ncdf_file_timestep("SICOMO", 8, sim_dict[eid], m, **contourf_opts)

    for ax, eid, l in zip(axs[3,:], ["Eem130-S2", "Eem125-S2", "Eem120-S2"], [True, False, False]):
       p2 = plot_overturning_anom_contours(amoc_dict[eid], amoc_dict["EXP003"], ax, labels=l, **amoc_anom_opts) 

    plot_overturning_contours(amoc_dict["EXP003"], axs[3, -1], labels=False, **amoc_abs_opts)

    axs[3, 0].ticklabel_format(style="sci", axis="y")
    [a.yaxis.set_ticklabels([]) for a in axs[-1, 1:]]

    f.subplots_adjust(bottom=0.20, wspace=0.05, hspace=0.05, left=0.15, right=0.95, top=0.95)
    cbar_ax = f.add_axes([0.15, 0.1, 1-0.15*2, 0.025])
    cbar = f.colorbar(p1, cax=cbar_ax, label="Sea Ice Concentration", orientation='horizontal',
                      norm=contourf_opts["levels"],
                      boundaries=[contourf_opts["levels"][0]*1.1]+contourf_opts["levels"]+[contourf_opts["levels"][-1]*1.1],
                      ticks=contourf_opts["levels"],
                      spacing="proportional")
    cbar.ax.set_xticklabels(contourf_opts["levels"], rotation=45.0, size="medium")

    # cbar2_ax = f.add_axes([0.15, 0.1, 1-0.15*2, 0.025])
    # cbar2 = f.colorbar(p2, cax=cbar2_ax, label="Atlantic Meridional Overturning Circulation Strength", orientation='horizontal',
    #                   norm=amoc_anom_opts["levels"],
    #                   boundaries=[amoc_anom_opts["levels"][0]*1.1]+amoc_anom_opts["levels"]+[amoc_anom_opts["levels"][-1]*1.1],
    #                   ticks=amoc_anom_opts["levels"],
    #                   spacing="proportional")
    # cbar2.ax.set_xticklabels(amoc_anom_opts["levels"], rotation=45.0, size="xx-small")
    plt.show()

    
