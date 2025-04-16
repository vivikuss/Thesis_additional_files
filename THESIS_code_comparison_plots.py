import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

### ADJUST THIS PART ###
# Paths
results_folder = '/Users/new/Desktop/THESIS'
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
        path_p = in_path + f'{star}/plev.out'
        data_p = np.loadtxt(path_p,skiprows=1)
        path_T = in_path + f'{star}/Tlev.out'
        data_T = np.loadtxt(path_T,skiprows=1)
        path_h = in_path + f'{star}/height.out'
        data_h = np.loadtxt(path_h,skiprows=1)

        row, column = j, 0  # top row
        ax1 = axs[row][column]
        row, column = j, 1  # bottom row
        ax2 = axs[row][column]

        ax1.semilogy(data_T, data_p, color = col, label = lab)          # pressure/temperature plot
        ax2.plot(data_T, 1e-3*data_h, color = col, label = lab)         # convert to km, altitude/temperature plot
        ax1.grid(True)
        ax2.grid(True)
        ax1.legend(loc='best',fontsize=17)
        ax2.legend(loc='best',fontsize=17)
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
#ax2.ticklabel_format(style='sci',axis='y')
#plt.suptitle(r"Comparison between H$_2$, N$_2$, He (700 W/m$^2$), M-dwarf spectrum")
plt.savefig('comparison_plot_h2_n2_he.png',dpi=750)
plt.show()