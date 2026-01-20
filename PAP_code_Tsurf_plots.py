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
axis_std = np.linspace(0.15,0.55,grid_size)
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
user = f"/Users/new/Desktop/"             #### CUSTOMIZE ####                            # path to Desktop
path = user + f"Thesis_Data/results_Tsurf_fin_1bar_"                                     # data for 1 bar
path2 = user + f"Thesis_Data/"                                                      # data from one-shot mode
path_20bar = user + f"Thesis_Data/results_Tsurf_"                                    # data for 20 bar
####

#### ADJUST LABELS AND PATHS FOR 20 BAR FURTHER DOWN ###

Tsurf = np.zeros((grid_size,grid_size))
flux = np.zeros((grid_size,grid_size))
albedo = np.zeros((grid_size,))
nu = np.linspace(1,50000,2000)
ASR = np.zeros((grid_size,))

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
for label,s,col,line in zip(labs1,strings,colors1,linestyles):      
    g = gas[0]                                                  # loop over concentrations for first gas
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)               # determine initial flux for label
        flux_label = round(flux[0,i],2)                                 # round
        try:
            data_T = np.loadtxt(path + f"{g}_{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            data_T = np.array(data_T)
            Tsurf[0,i] = data_T
            isr = np.loadtxt(path + f"{g}_{s}_{flux_label}/ISR.out", skiprows=1)
            isr = np.array(isr)
            flux[0,i] = 4.0*isr[-1]                                     # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit           # determine semi major axis from flux
        except Exception as e:                                            # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    # Use one-shot mode to add data for flux = 120, 1200 W/m2 cases
    tsurf_1200 = np.loadtxt(path2+f'results_add_1200_{g}_{s}/Tsurf_final.out',skiprows=0)
    isr_1200 = np.loadtxt(path2+f'results_add_1200_{g}_{s}/ISR.out',skiprows=1)
    axis_1200 = np.sqrt(lum_si[0]/(4*np.pi*4.0*isr_1200[-1]))
    Tsurf_new = np.append(Tsurf[0,:], tsurf_1200)
    axis_new = np.append(axis_adj, axis_1200/au_unit)

    tsurf_120 = np.loadtxt(path2+f'results_add_low_{g}_{s}/Tsurf_final.out',skiprows=0)
    isr_120 = np.loadtxt(path2+f'results_add_low_{g}_{s}/ISR.out',skiprows=1)
    axis_120 = np.sqrt(lum_si[0]/(4*np.pi*4.0*isr_120[-1]))
    Tsurf_new = np.append(Tsurf_new, tsurf_120)
    axis_new = np.append(axis_new, axis_120/au_unit)

    sorted_indices = np.argsort(axis_new)
    Tsurf_new = Tsurf_new[sorted_indices]
    axis_new = axis_new[sorted_indices]

    ax1.plot(axis_new, Tsurf_new,label={label},color=col,linestyle=line)
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
            isr = np.loadtxt(path + f"{g}_{s}_{flux_label}/ISR.out", skiprows=1)
            isr = np.array(isr)
            flux[0,i] = 4.0*isr[-1]                                          # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit            # determine semi major axis from flux
        except Exception as e:                                                  # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    # Use data from one-shot mode to add data for flux = 120, 1200 W/m2 cases
    tsurf_1200 = np.loadtxt(path2+f'results_add_1200_{g}_{s}/Tsurf_final.out',skiprows=0)
    isr_1200 = np.loadtxt(path2+f'results_add_1200_{g}_{s}/ISR.out',skiprows=1)
    axis_1200 = np.sqrt(lum_si[0]/(4*np.pi*4.0*isr_1200[-1]))
    Tsurf_new = np.append(Tsurf[0,:], tsurf_1200)
    axis_new = np.append(axis_adj, axis_1200/au_unit)

    tsurf_120 = np.loadtxt(path2+f'results_add_low_{g}_{s}/Tsurf_final.out',skiprows=0)
    isr_120 = np.loadtxt(path2+f'results_add_low_{g}_{s}/ISR.out',skiprows=1)
    axis_120 = np.sqrt(lum_si[0]/(4*np.pi*4.0*isr_120[-1]))
    Tsurf_new = np.append(Tsurf_new, tsurf_120)
    axis_new = np.append(axis_new, axis_120/au_unit)

    sorted_indices = np.argsort(axis_new)
    Tsurf_new = Tsurf_new[sorted_indices]
    axis_new = axis_new[sorted_indices]

    ax1.plot(axis_new, Tsurf_new,label={label},color=col,linestyle=line)
    secax1 = ax1.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))    # add second x axis for flux
    secax1.tick_params(axis='x', labelsize=18, pad=2)
    secax1.set_xticks([150, 300, 600, 1200])

ax1.grid(True, which='both')
ax1.xaxis.set_major_formatter(formatter)
ax1.xaxis.offsetText.set_horizontalalignment('right')
ax1.set_xlabel('Semi Major Axis (au)',fontsize=18)
ax1.set_ylabel(r'T$_{surf}$ (K)',fontsize=18)
secax1.set_xlabel(r'Flux (W/m$^2$)', fontsize=18, labelpad=10)

### CUSTOMIZE IF NEEDED ###
# Labels for 20 bar case
# labs1 = [r'20 bar, 99% He,   1% CO$_2$',r'20 bar, 90% He, 10% CO$_2$',r'20 bar,   5% He, 95% CO$_2$']
# labs2 = [r'20 bar, 99% H$_2$,   1% CO$_2$',r'20 bar, 90% H$_2$, 10% CO$_2$',r'20 bar,   5% H$_2$, 95% CO$_2$']
strings1 = ['he_20bar_1p','he_10p_20bar_10p','he_20bar_95p']   # ideally, these files are named more coherently :')
strings2 = ['h2_20bar_1p','h2_10p_20bar_10p','h2_20bar_95p']
colors1 = ['darkviolet', 'indigo','rebeccapurple']
colors2 = ['orange', 'coral','maroon']
linestyles = ['solid', 'dashed', 'dotted']
### 

### ADJUST THIS PART ###
# Path for 20 bar case
path = f"/Users/new/Desktop/Thesis_Data/results_Tsurf_"
###
ax2.fill_between(axis_std, temps[0]*np.ones_like(axis), temps[1]*np.ones_like(axis),color='paleturquoise', label='Habitable Zone')
for label,s,col,line in zip(labs1,strings1,colors1,linestyles):             # loop over concentrations for first gas
    for i in range(grid_size):  
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                    # determine initial flux for label
        flux_label = round(flux[0,i],2)                                     # round
        try:
            data_T = np.loadtxt(path + f"{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            data_T = np.array(data_T)
            Tsurf[0,i] = data_T
            isr = np.loadtxt(path + f"{s}_{flux_label}/ISR.out", skiprows=1)
            isr = np.array(isr)
            flux[0,i] = 4.0*isr[-1]                                                  # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux
        except Exception as e:                                                          # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    # Use data from one-shot mode to add data for flux = 120 W/m2 case
    tsurf_120 = np.loadtxt(path2+f'results_add_low_{s}/Tsurf_final.out',skiprows=0)
    isr_120 = np.loadtxt(path2+f'results_add_low_{s}/ISR.out',skiprows=1)
    axis_120 = np.sqrt(lum_si[0]/(4*np.pi*4.0*isr_120[-1]))
    Tsurf_new = np.append(Tsurf[0,:], tsurf_120)
    axis_new = np.append(axis_adj, axis_120/au_unit)

    sorted_indices = np.argsort(axis_new)
    Tsurf_new = Tsurf_new[sorted_indices]
    axis_new = axis_new[sorted_indices]

    ax2.plot(axis_new, Tsurf_new,label={label},color=col,linestyle=line)
    secax2 = ax2.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))     # add second x axis for flux
    secax2.tick_params(axis='x', labelsize=18, pad=2)
    secax2.set_xticks([150, 300, 600, 1200])


for label,s,col,line in zip(labs2,strings2,colors2,linestyles):          # loop over concentrations for second gas
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_T = np.loadtxt(path + f"{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            Tsurf[0,i] = data_T#[0]
            isr = np.loadtxt(path + f"{s}_{flux_label}/ISR.out", skiprows=1)
            isr = np.array(isr)
            flux[0,i] = 4.0*isr[-1]                                              # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux
        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan
    
    ax2.plot(axis_adj, Tsurf[0,:],label={label},color=col,linestyle=line)
    secax2 = ax2.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))    # add second x axis for flux
    secax2.tick_params(axis='x', labelsize=18, pad=2)
    secax2.set_xticks([150, 300, 600, 1200])

ax2.grid(True, which='both')
ax2.xaxis.set_major_formatter(formatter)
ax2.xaxis.offsetText.set_horizontalalignment('right')
ax2.set_xlabel('Semi Major Axis (au)',fontsize=18)
secax2.set_xlabel(r'Flux (W/m$^2$)', fontsize=18, labelpad=10)
ax1.set_xticks([0.2, 0.3, 0.4, 0.5])
ax2.set_xticks([0.2, 0.3, 0.4, 0.5])
ax1.tick_params(labelsize=17)
ax2.tick_params(labelsize=17)
ax1.text(0.54, 0.68, 'Habitable Zone', transform=ax1.transAxes,fontsize=18,fontweight='bold',color='lightseagreen')   
ax2.text(0.54, 0.68, 'Habitable Zone', transform=ax2.transAxes,fontsize=18,fontweight='bold',color='lightseagreen')   
ax1.text(-0.15, 1.05, 'a)', transform=ax1.transAxes,fontsize=20,fontweight='bold',va='bottom', ha='left')
ax2.text(-0.10, 1.05, 'b)', transform=ax2.transAxes,fontsize=20,fontweight='bold',va='bottom', ha='left')
plt.subplots_adjust(bottom=0.16)  

for label,s,col,line in zip(labs1,strings1,colors1,linestyles):             # loop over concentrations for first gas
    for i in range(grid_size):  
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_asr = np.loadtxt(path_20bar + f"{s}_{flux_label}/ASR.out", skiprows=1) 
            ASR[i] = data_asr[-1]
            data_isr = np.loadtxt(path_20bar + f"{s}_{flux_label}/ISR.out", skiprows=1) 
            ISR = data_isr[-1]
            OSR = ISR-ASR[i]
            albedo[i] = OSR/ISR
            flux[0,i] = 4.0*ISR                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux
        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            ASR[i] = np.nan
    ax3.plot(axis_adj, albedo, label=label, color=col, linewidth=2, linestyle=line)

for label,s,col,line in zip(labs2,strings2,colors2,linestyles):          # loop over concentrations for second gas
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_asr = np.loadtxt(path_20bar + f"{s}_{flux_label}/ASR.out", skiprows=1) 
            ASR[i] = data_asr[-1]
            data_isr = np.loadtxt(path_20bar + f"{s}_{flux_label}/ISR.out", skiprows=1) 
            ISR = data_isr[-1]
            OSR = ISR-ASR[i]
            albedo[i] = OSR/ISR
            flux[0,i] = 4.0*ISR                                            # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))/au_unit                    # determine semi major axis from flux
        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            ASR[i] = np.nan
    
    ax3.plot(axis_adj, albedo, label=label, color=col, linewidth=2, linestyle=line)

ax3.text(-0.10, 1.05, 'c)', transform=ax3.transAxes,fontsize=20,fontweight='bold',va='bottom', ha='left')
ax3.grid(True, which='both')
ax3.xaxis.set_major_formatter(formatter)
ax3.xaxis.offsetText.set_horizontalalignment('right')
ax3.set_xlabel('Semi Major Axis (au)',fontsize=18)
ax3.set_ylabel('Albedo', fontsize=18)
ax3.set_xticks([0.2, 0.3, 0.4, 0.5])
ax3.set_yticks([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
ax3.set_xlim([0.15,0.55]) 
ax3.tick_params(labelsize=18)
ax3.legend(loc='best', fontsize=18)

ax1.fill_between(axis_std, temps[0]*np.ones_like(axis), temps[1]*np.ones_like(axis),color='paleturquoise', label='Habitable Zone')

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.savefig(user + 'surface_temperatures_1bar_20bar_he_h2_added.png',dpi=750)
plt.show()
