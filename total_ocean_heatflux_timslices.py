#!/usr/bin/env python
import matplotlib.pyplot as plt
from basemap_wrappers.basemap_nhem import map_nhem
# from custom_io.get_remote_data import get_remote_data
from plot_tools import plot_var_from_ncdf_file_timestep
import numpy as np
from simulation_tools import cosmos_standard_analysis

exps = [line.strip() for line in open("/Users/pgierz/Research/Eem_Hol_Wiso/exps.dat", 'r') if "#" not in line]
expids = [e.split("/")[-1] for e in exps]


def import_required_data_seaice_concentration():
    sim_dict = {}
    for exp, eid in zip(exps, expids):
        path = "/".join(exp.split(":")[-1].split("/")[:-1])
        # print path
        f = cosmos_standard_analysis("pgierz", "stan1", path, eid).ymonmean("FLUM")
        # print f
        sim_dict[eid] = f
    return sim_dict


contourf_opts = {
    "cmap": plt.cm.RdBu_r,
    "levels": np.arange(-250, 270, 20)
}

if __name__ == '__main__':
    sim_dict = import_required_data_seaice_concentration()
    
    f, axs = plt.subplots(3, 4)

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
        plot_var_from_ncdf_file_timestep("FLUM", 2, sim_dict[eid], m, **contourf_opts)

    for ax, eid in zip(axs[1, :], expids):
        m = map_nhem(thisax=ax, fill_color=None, coastlines=False)
        plot_var_from_ncdf_file_timestep("FLUM", 5, sim_dict[eid], m, **contourf_opts)

    for ax, eid in zip(axs[2, :], expids):
        m = map_nhem(thisax=ax, fill_color=None, coastlines=False)
        p1 = plot_var_from_ncdf_file_timestep("FLUM", 8, sim_dict[eid], m, **contourf_opts)

    f.subplots_adjust(bottom=0.30, wspace=0.05, hspace=0.05, left=0.05, right=0.95)
    cbar_ax = f.add_axes([0.15, 0.20, 1-0.15*2.0, 0.025])
    cbar = f.colorbar(p1, cax=cbar_ax, label=r"Ocean Heat Flux [W/m$^{2}$]", orientation='horizontal',
                      norm=contourf_opts["levels"],
                      boundaries=[contourf_opts["levels"][0]*1.1]+contourf_opts["levels"]+[contourf_opts["levels"][-1]*1.1],
                      ticks=contourf_opts["levels"],
                      spacing="proportional")
    cbar.ax.set_xticklabels(contourf_opts["levels"], rotation=45.0, size="xx-small")


    f, axs = plt.subplots(2, 2)
    
    
    plt.show()

