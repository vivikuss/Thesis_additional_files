import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

### ADJUST THIS PART ###
# Paths
user = f"/Users/new/Desktop/"   #### CUSTOMIZE ####
results_folder = user + 'Thesis_Data/'
paths = ['results_hybrid_h2_', 'results_hybrid_n2_', 'results_hybrid_he_']
colors = ['coral','deepskyblue','darkviolet']
labels = [r'99% H$_2$, 1% CO$_2$, 1 bar',r'99% N$_2$, 1% CO$_2$, 1 bar',r'99% He, 1% CO$_2$, 1 bar']
spectra = ['solar', 'mdwarf']
###

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(17, 15), sharex=True, sharey='col')
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))
plt.rcParams.update({'font.size': 13})

for j, star in enumerate(spectra):
    for k, (col,in_path,lab) in enumerate(zip(colors,paths,labels)):
        path_p = results_folder + in_path + f'{star}/plev.out'
        data_p = np.loadtxt(path_p,skiprows=1)
        path_T = results_folder + in_path + f'{star}/Tlev.out'
        data_T = np.loadtxt(path_T,skiprows=1)
        path_h = results_folder + in_path + f'{star}/height.out'
        data_h = np.loadtxt(path_h,skiprows=1)

        row, column = j, 0  # top row
        ax1 = axs[row][column]
        row, column = j, 1  # bottom row
        ax2 = axs[row][column]

        ax1.semilogy(data_T, data_p, color = col, label = lab, linewidth = 2.5)          # pressure/temperature plot
        ax2.plot(data_T, 1e-3*data_h, color = col, label = lab, linewidth = 2.5)         # convert to km, altitude/temperature plot
        ax1.grid(True)
        ax2.grid(True)
        if j==0: 
             ax1.legend(loc='best',fontsize=17)
        #ax2.legend(loc='best',fontsize=17)
        ax1.tick_params(labelsize=17)
        ax2.tick_params(labelsize=17)

        ax1.set_xlabel('Temperature (K)',fontsize=17)
        ax1.set_ylabel('Pressure (Pa)',fontsize=17)
        ax2.set_xlabel('Temperature (K)',fontsize=17)
        ax2.set_ylabel('Altitude (km)',fontsize=17)

        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(False)   # Force scientific notation
        formatter.set_powerlimits((-1, 1))   
        ax2.yaxis.set_major_formatter(formatter)

ax1.invert_yaxis()
fig.subplots_adjust(hspace=0.4)
fig.text(0.5, 0.96, "G Dwarf Spectrum", ha="center", va="top", fontweight='bold', fontsize=20)
fig.text(0.5, 0.50, "M Dwarf Spectrum", ha="center", va="top", fontweight='bold', fontsize=20)
labels_sub = ['a)', 'b)', 'c)', 'd)']
positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
offsets = [(-0.15, 1.05), (-0.10, 1.05), (-0.15, 1.05), (-0.10, 1.05)]
for label, (i, j), (x, y) in zip(labels_sub, positions, offsets):
    axs[i, j].text(x, y, label, transform=axs[i,j].transAxes,fontsize=20,va='bottom', ha='left')
plt.savefig(user + 'combined_comparison_pap_new.png',dpi=750)
plt.show()
