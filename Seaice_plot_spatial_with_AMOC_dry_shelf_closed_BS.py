#!/usr/bin/env python
import matplotlib.pyplot as plt
from basemap_wrappers.basemap_nhem import map_nhem
from plot_tools import plot_var_from_ncdf_file_timestep
import numpy as np
from simulation_tools import cosmos_standard_analysis

expids = ["Eem130-S2", "LIG130_dles_nbs_w", "EXP003"]

user = "pgierz"
host = "stan1"
path1 = "/ace/user/pgierz/cosmos-aso-wiso/"
path2 = "/ace/user/pgierz/cosmos-aso"


def import_required_data_seaice_concentration():
    return {"Eem130-S2": cosmos_standard_analysis(user, host, path1, "Eem130-S2").ymonmean("SICOMO"),
            "LIG130_dles_nbs_w": cosmos_standard_analysis(user, host, path2, "LIG130_dles_nbs_w").ymonmean("SICOMO"),
            "EXP003": cosmos_standard_analysis(user, host, path1, "EXP003").ymonmean("SICOMO")}


contourf_opts = {
    "cmap": plt.cm.jet,
    "levels": np.arange(0, 1.05, 0.05)
}

if __name__ == '__main__':
    sim_dict = import_required_data_seaice_concentration()

    f, axs = plt.subplots(3, 3)

    # Set Titles
    axs[0, 0].set_title("LIG-130")
    axs[0, 1].set_title("LIG-130 Dry Shelf/Closed BS")
    axs[0, 2].set_title("PI")
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

    f.subplots_adjust(bottom=0.20, wspace=0.05, hspace=0.05, left=0.15, right=0.95, top=0.95)
    cbar_ax = f.add_axes([0.15, 0.1, 1-0.15*2, 0.025])
    cbar = f.colorbar(p1, cax=cbar_ax, label="Sea Ice Concentration", orientation='horizontal',
                      norm=contourf_opts["levels"],
                      boundaries=[contourf_opts["levels"][0]*1.1]+contourf_opts["levels"]+[contourf_opts["levels"][-1]*1.1],
                      ticks=contourf_opts["levels"],
                      spacing="proportional")
    cbar.ax.set_xticklabels(contourf_opts["levels"], rotation=45.0, size="medium")

    plt.show()
