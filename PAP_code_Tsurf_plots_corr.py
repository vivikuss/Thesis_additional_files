import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# create grid
au_unit = 1.5e11        # m
Lsun_unit = 3.846e26    # Watts
grid_size = 10          # number of data points

### CUSTOMIZE IF NEEDED ###
# stellar luminosity and semi major axis range
axis_si = np.linspace(0.15,0.65,grid_size)*au_unit      # in meters
lum_si = np.ones_like(axis_si)*0.0234*Lsun_unit         # in Watts
axis = np.linspace(0.15,0.65,grid_size)                # in au
lum = np.ones_like(axis_si)*0.0234                      # in Lsun
axis_adj = np.zeros_like(axis)                          # account for adjusted scheme in PCM_LBL
x,y = np.meshgrid(axis,lum)
axis_std = np.linspace(0.15,0.65,grid_size)
###

### CUSTOMIZE IF NEEDED ###
# Labels for 1 bar case
gas = ['He_', 'H2_']      # He or H2 atmosphere
co2 = [0.01, 0.1, 0.95]     # CO2 concentrations
h = [0.99, 0.9, 0.05]      # He or H2 concentrations
strings = ['1p','10p','95p']    # labels for path
labs1 = [r'99% He,   1% CO$_2$',r'90% He, 10% CO$_2$',r'  5% He, 95% CO$_2$']               # labels for plot
labs2 = [r'99% H$_2$,   1% CO$_2$',r'90% H$_2$, 10% CO$_2$',r'  5% H$_2$, 95% CO$_2$']       # labels for plot
colors1 = ['darkviolet', 'indigo','rebeccapurple']
colors2 = ['orange', 'coral','maroon']
linestyles = ['solid', 'dashed', 'dotted']
temps = [273.15, 373.15]
###

### ADJUST THIS PART ###
# Path for all cases
user = f"/Users/new/Dropbox/Desktop/"
path = user + f"Thesis_Data/results_Tsurf_fin_1bar_"                                     # data for 1 bar
path2 = user + f"Thesis_Data/"                                  # data from one-shot mode
path_20bar = user + f"Thesis_Data/results_Tsurf_"                                    # data for 20 bar
####

#### ADJUST LABELS AND PATHS FOR 20 BAR FURTHER DOWN ###

Tsurf = np.zeros((grid_size,grid_size))
flux = np.zeros((grid_size,grid_size))
albedo = np.zeros((grid_size,))
nu = np.linspace(1,50000,2000)
ASR = np.zeros((grid_size,))
dnu = nu[2]-nu[1]

# convert axis to flux and flux to axis for fixed luminosity
def axis_to_flux(axis):
    axis_si = axis*au_unit
    return lum_si[0]/(4*np.pi*axis_si**2)

def flux_to_axis(flux):
    return np.sqrt(lum_si[0]/(4*np.pi*flux))/(au_unit)

# Plot surface temperature in two panels
f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 9))
ax2.sharey(ax1)
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(False)  # force scientific notation
formatter.set_powerlimits((-1, 1))  
ax1.axvline(x=flux_to_axis(605),color="midnightblue",linewidth=2)
ax1.text(0.2, 0.83, 'LHS 1140 b', transform=ax1.transAxes,fontsize=17,color="midnightblue")
ax1.axvline(x=flux_to_axis(1368),color="dodgerblue",linewidth=2)
ax1.text(0.02, 0.18, 'K2-18b', transform=ax1.transAxes,fontsize=17,color="dodgerblue")
for label,s,col,line in zip(labs1,strings,colors1,linestyles):      
    g = gas[0]                                                  # loop over concentrations for first gas
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)               # determine initial flux for label
        flux_label = round(flux[0,i],2)                                 # round
        try:
            data_T = np.loadtxt(path + f"{g}_{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            data_T = np.array(data_T)
            Tsurf[0,i] = data_T
            
            data_isrnu = np.loadtxt(path + f"{g}_{s}_{flux_label}/ISRnu.out", skiprows=0)  # determine total ISR
            int_isr = 0
            for interval in range(nu.size):
                int_isr += data_isrnu[interval]
            int_isr *= dnu

            flux[0,i] = 4.0*int_isr                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit     # determine semi major axis from flux

        except Exception as e:                                            # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    # Use one-shot mode to add data for flux = 120, 1200 W/m2 cases
    tsurf_1200 = np.loadtxt(path2+f'results_add_1200_{g}_{s}/Tsurf_final.out',skiprows=0)
    data_isrnu = np.loadtxt(path2+f'results_add_1200_{g}_{s}/ISRnu.out', skiprows=0) 
    int_isr = 0
    for interval in range(nu.size):
        int_isr += data_isrnu[interval]
    int_isr *= dnu

    axis_1200 = np.sqrt(lum_si[0]/(4*np.pi*4.0*int_isr))   
    Tsurf_new = np.append(Tsurf[0,:], tsurf_1200)
    axis_new = np.append(axis_adj, axis_1200/au_unit)

    sorted_indices = np.argsort(axis_new)
    Tsurf_new = Tsurf_new[sorted_indices]
    axis_new = axis_new[sorted_indices]

    ax1.plot(axis_new, Tsurf_new,label={label},color=col,linestyle=line,linewidth=2)
    secax1 = ax1.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))     # add second x axis for flux
    secax1.tick_params(axis='x', labelsize=18, pad=2)
    secax1.set_xticks([150, 300, 600, 1200])

for label,s,col,line in zip(labs2,strings,colors2,linestyles):
    g = gas[1]                                                          # loop over concentrations for second gas
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                       # determine initial flux for label
        flux_label = round(flux[0,i],2)                                   # round
        try:
            data_T = np.loadtxt(path + f"{g}_{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            data_T = np.array(data_T)
            Tsurf[0,i] = data_T

            data_isrnu = np.loadtxt(path + f"{g}_{s}_{flux_label}/ISRnu.out", skiprows=0)  # determine total ISR
            int_isr = 0
            for interval in range(nu.size):
                int_isr += data_isrnu[interval]
            int_isr *= dnu

            flux[0,i] = 4.0*int_isr                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit        # determine semi major axis from flux

        except Exception as e:                                                  # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    # Use data from one-shot mode to add data for flux = 120, 1200 W/m2 cases
    tsurf_1200 = np.loadtxt(path2+f'results_add_1200_{g}_{s}/Tsurf_final.out',skiprows=0)
    data_isrnu = np.loadtxt(path2+f'results_add_1200_{g}_{s}/ISRnu.out', skiprows=0) 
    int_isr = 0
    for interval in range(nu.size):
        int_isr += data_isrnu[interval]
    int_isr *= dnu

    axis_1200 = np.sqrt(lum_si[0]/(4*np.pi*4.0*int_isr))
    Tsurf_new = np.append(Tsurf[0,:], tsurf_1200)
    axis_new = np.append(axis_adj, axis_1200/au_unit)

    sorted_indices = np.argsort(axis_new)
    Tsurf_new = Tsurf_new[sorted_indices]
    axis_new = axis_new[sorted_indices]

    ax1.plot(axis_new, Tsurf_new, label={label},color=col,linestyle=line,linewidth=2)
    secax1 = ax1.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))    # add second x axis for flux
    secax1.tick_params(axis='x', labelsize=18, pad=2)
    secax1.set_xticks([150, 300, 600, 1200])

ax1.grid(True, which='both')
ax1.xaxis.set_major_formatter(formatter)
ax1.xaxis.offsetText.set_horizontalalignment('right')
ax1.set_xlabel('Semi Major Axis (au)',fontsize=22)
ax1.set_ylabel(r'T$_{surf}$ (K)',fontsize=22)
secax1.set_xlabel(r'Flux (W/m$^2$)', fontsize=22, labelpad=10)

### CUSTOMIZE IF NEEDED ###
# Labels for 20 bar case
strings1 = ['he_20bar_1p','he_10p_20bar_10p','he_20bar_95p']   # ideally, these files are named more coherently :')
strings2 = ['h2_20bar_1p','h2_10p_20bar_10p','h2_20bar_95p']
colors1 = ['darkviolet', 'indigo','rebeccapurple']
colors2 = ['orange', 'coral','maroon']
linestyles = ['solid', 'dashed', 'dotted']
### 

### ADJUST THIS PART ###
# Path for 20 bar case
path = user + f"Thesis_Data/results_Tsurf_"
###
ax2.fill_between(axis_std, temps[0]*np.ones_like(axis), temps[1]*np.ones_like(axis),color='paleturquoise', label='Habitable Zone')
ax2.axvline(x=flux_to_axis(605),color="midnightblue",linewidth=2)
ax2.text(0.2, 0.83, 'LHS 1140 b', transform=ax2.transAxes,fontsize=17,color="midnightblue")
ax2.axvline(x=flux_to_axis(1368),color="dodgerblue",linewidth=2)
ax2.text(0.02, 0.18, 'K2-18b', transform=ax2.transAxes,fontsize=17,color="dodgerblue")
for label,s,col,line in zip(labs1,strings1,colors1,linestyles):             # loop over concentrations for first gas
    flux = np.zeros((grid_size,grid_size))
    for i in range(grid_size):  
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                    # determine initial flux for label
        flux_label = round(flux[0,i],2)                                     # round
        try:
            data_T = np.loadtxt(path + f"{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            data_T = np.array(data_T)
            Tsurf[0,i] = data_T

            data_isrnu = np.loadtxt(path + f"{s}_{flux_label}/ISRnu.out", skiprows=0)  # determine total ISR
            int_isr = 0
            for interval in range(nu.size):
                int_isr += data_isrnu[interval]
            int_isr *= dnu

            flux[0,i] = 4.0*int_isr                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit         # determine semi major axis from flux

        except Exception as e:                                                          # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    ax2.plot(axis_adj, Tsurf[0,:],label={label},color=col,linestyle=line,linewidth=2)
    secax2 = ax2.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))     # add second x axis for flux
    secax2.tick_params(axis='x', labelsize=18, pad=2)
    secax2.set_xticks([150, 300, 600, 1200])


for label,s,col,line in zip(labs2,strings2,colors2,linestyles):          # loop over concentrations for second gas
    flux = np.zeros((grid_size,grid_size))
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_T = np.loadtxt(path + f"{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            Tsurf[0,i] = data_T

            data_isrnu = np.loadtxt(path + f"{s}_{flux_label}/ISRnu.out", skiprows=0)  # determine total ISR
            int_isr = 0
            for interval in range(nu.size):
                int_isr += data_isrnu[interval]
            int_isr *= dnu

            flux[0,i] = 4.0*int_isr                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux

        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan
    
    ax2.plot(axis_adj, Tsurf[0,:],label={label},color=col,linestyle=line,linewidth=2)
    secax2 = ax2.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))    # add second x axis for flux
    secax2.tick_params(axis='x', labelsize=18, pad=2)
    secax2.set_xticks([150, 300, 600, 1200])

ax2.grid(True, which='both')
ax2.xaxis.set_major_formatter(formatter)
ax2.xaxis.offsetText.set_horizontalalignment('right')
ax2.set_xlabel('Semi Major Axis (au)',fontsize=22)
secax2.set_xlabel(r'Flux (W/m$^2$)', fontsize=22, labelpad=10)
ax1.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6])
ax2.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6])
ax1.tick_params(labelsize=22)
ax2.tick_params(labelsize=22)
ax1.text(0.48, 0.63, 'Habitable Zone', transform=ax1.transAxes,fontsize=21,fontweight='bold',color='lightseagreen')   
ax2.text(0.48, 0.63, 'Habitable Zone', transform=ax2.transAxes,fontsize=21,fontweight='bold',color='lightseagreen')   
ax1.text(-0.15, 1.07, 'a) 1 bar', transform=ax1.transAxes,fontsize=22,fontweight='bold',va='bottom', ha='left')
ax2.text(-0.10, 1.07, 'b) 20 bar', transform=ax2.transAxes,fontsize=22,fontweight='bold',va='bottom', ha='left')
plt.subplots_adjust(bottom=0.16)  

for label,s,col,line in zip(labs1,strings1,colors1,linestyles):             # loop over concentrations for first gas
    axis_adj = np.zeros_like(axis)
    albedo = np.zeros((grid_size,))
    for i in range(grid_size):  
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_isrnu = np.loadtxt(path_20bar + f"{s}_{flux_label}/ISRnu.out", skiprows=0) 
            data_osrnu = np.loadtxt(path_20bar + f"{s}_{flux_label}/OSRnu.out", skiprows=1) 

            int_isr, int_osr = 0, 0                                     # determine total ISR and OSR
            for interval in range(nu.size):
                int_isr += data_isrnu[interval]
                int_osr += data_osrnu[interval]
            int_isr *= dnu
            int_osr *= dnu
            albedo[i] = int_osr/int_isr

            flux[0,i] = 4.0*int_isr                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux

        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan
 
    ax3.plot(axis_adj, albedo, label=label, color=col, linewidth=2, linestyle=line)

for label,s,col,line in zip(labs2,strings2,colors2,linestyles):          # loop over concentrations for second gas
    axis_adj = np.zeros_like(axis)
    albedo = np.zeros((grid_size,))
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_isrnu = np.loadtxt(path_20bar + f"{s}_{flux_label}/ISRnu.out", skiprows=0) 
            data_osrnu = np.loadtxt(path_20bar + f"{s}_{flux_label}/OSRnu.out", skiprows=1) 

            int_isr, int_osr = 0, 0                                 # determine total ISR and OSR
            for interval in range(nu.size):
                int_isr += data_isrnu[interval]
                int_osr += data_osrnu[interval]
            int_isr *= dnu
            int_osr *= dnu
            albedo[i] = int_osr/int_isr

            flux[0,i] = 4.0*int_isr                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux

        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan
   
    ax3.plot(axis_adj, albedo, label=label, color=col, linewidth=2, linestyle=line)

ax3.text(-0.10, 1.07, 'c) Albedo', transform=ax3.transAxes,fontsize=22,fontweight='bold',va='bottom', ha='left')
ax3.grid(True, which='both')
ax3.xaxis.set_major_formatter(formatter)
ax3.xaxis.offsetText.set_horizontalalignment('right')
ax3.set_xlabel('Semi Major Axis (au)',fontsize=22)
ax3.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6])
ax3.set_yticks([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
ax3.tick_params(labelsize=22)
ax3.legend(loc='best', fontsize=21)

ax1.fill_between(axis_std, temps[0]*np.ones_like(axis), temps[1]*np.ones_like(axis),color='paleturquoise', label='Habitable Zone')

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.savefig('/Users/new/Desktop/surface_temperatures_1bar_20bar_he_h2_corrected_ISR.png',dpi=750)
plt.show()
