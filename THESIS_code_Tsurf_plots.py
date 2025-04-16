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
###

### CUSTOMIZE IF NEEDED ###
# Labels for 1 bar case
gas = ['He_', 'H2_']      # He or H2 atmosphere
strings = ['1p','10p','95p']    # labels for path
labs1 = [r'1 bar, 99% He,   1% CO$_2$',r'1 bar, 90% He, 10% CO$_2$',r'1 bar,   5% He, 95% CO$_2$'] # labels for plot
labs2 = [r'1 bar, 99% H$_2$,   1% CO$_2$',r'1 bar, 90% H$_2$, 10% CO$_2$',r'1 bar,   5% H$_2$, 95% CO$_2$'] # labels for plot
colors1 = ['darkviolet', 'indigo','rebeccapurple']
colors2 = ['orange', 'coral','maroon']
linestyles = ['solid', 'dashed', 'dotted']
###

### ADJUST THIS PART ###
# Path for 1 bar case
path = f"/Users/new/Desktop/THESIS/THESIS_PCM_LBL/example_run/results_Tsurf_1bar_"
####

#### ADJUST LABELS AND PATHS FOR 20 BAR FURTHER DOWN ###

Tsurf = np.zeros((grid_size,grid_size))
flux = np.zeros((grid_size,grid_size))

# convert axis to flux and flux to axis for fixed luminosity
def axis_to_flux(axis):
    axis_si = axis*au_unit
    return lum_si[0]/(4*np.pi*axis_si**2)

def flux_to_axis(flux):
    return np.sqrt(lum_si[0]/(4*np.pi*flux))/(au_unit)

# Plot surface temperature in two panels
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 5))
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
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))           # determine semi major axis from flux
        except Exception as e:                                            # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    ax1.plot(axis, Tsurf[0,:],label={label},color=col,linestyle=line)
    secax1 = ax1.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))     # add second x axis for flux
    secax1.tick_params(axis='x', labelsize=11, pad=5)
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
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))            # determine semi major axis from flux
        except Exception as e:                                                  # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    ax1.plot(axis, Tsurf[0,:],label={label},color=col,linestyle=line)
    secax1 = ax1.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))    # add second x axis for flux
    secax1.tick_params(axis='x', labelsize=11, pad=5)
    secax1.set_xticks([150, 300, 600, 1200])

ax1.grid(True, which='both')
ax1.legend(loc='best')
ax1.xaxis.set_major_formatter(formatter)
ax1.xaxis.offsetText.set_horizontalalignment('right')
ax1.set_xlabel('Semi Major Axis (au)',fontsize=13)
ax1.set_ylabel(r'T$_{surf}$ (K)',fontsize=13)
secax1.set_xlabel(r'Flux (W/m$^2$)', fontsize=13, labelpad=10)

### CUSTOMIZE IF NEEDED ###
# Labels for 20 bar case
gas = ['He_', 'H2_']      # He or H2 atmosphere
strings = ['1p','10p','95p']    # labels for path
labs1 = [r'20 bar, 99% He,   1% CO$_2$',r'20 bar, 90% He, 10% CO$_2$',r'20 bar,   5% He, 95% CO$_2$']
labs2 = [r'20 bar, 99% H$_2$,   1% CO$_2$',r'20 bar, 90% H$_2$, 10% CO$_2$',r'20 bar,   5% H$_2$, 95% CO$_2$']
colors1 = ['darkviolet', 'indigo','rebeccapurple']
colors2 = ['orange', 'coral','maroon']
linestyles = ['solid', 'dashed', 'dotted']
### 

### ADJUST THIS PART ###
# Path for 20 bar case
path = f"/Users/new/Desktop/THESIS/THESIS_PCM_LBL/example_run/results_Tsurf_20bar_"
###

for label,s,col,line in zip(labs1,strings,colors1,linestyles):             # loop over concentrations for first gas
    g = gas[0] 
    for i in range(grid_size):  
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                    # determine initial flux for label
        flux_label = round(flux[0,i],2)                                     # round
        try:
            data_T = np.loadtxt(path + f"{g}_{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            data_T = np.array(data_T)
            Tsurf[0,i] = data_T
            isr = np.loadtxt(path + f"{g}_{s}_{flux_label}/ISR.out", skiprows=1)
            isr = np.array(isr)
            flux[0,i] = 4.0*isr[-1]                                                  # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))                    # determine semi major axis from flux
        except Exception as e:                                                          # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan

    ax2.plot(axis, Tsurf[0,:],label={label},color=col,linestyle=line)
    secax2 = ax2.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))     # add second x axis for flux
    secax2.tick_params(axis='x', labelsize=11, pad=5)
    secax2.set_xticks([150, 300, 600, 1200])


for label,s,col,line in zip(labs2,strings,colors2,linestyles):          # loop over concentrations for second gas
    g = gas[1] 
    for i in range(grid_size):
        flux[0,i] = lum_si[0]/(4*np.pi*axis_si[i]**2)                   # determine initial flux for label
        flux_label = round(flux[0,i],2)                              # round
        try:
            data_T = np.loadtxt(path + f"{g}_{s}_{flux_label}/Tsurf_final.out", skiprows=0) 
            Tsurf[0,i] = data_T
            isr = np.loadtxt(path + f"{g}_{s}_{flux_label}/ISR.out", skiprows=1)
            isr = np.array(isr)
            flux[0,i] = 4.0*isr[-1]                                              # determine actual flux after adjustment in PCM_LBL
            axis_adj[i] = np.sqrt(lum_si[0]/(4*np.pi*flux[0,i]))                    # determine semi major axis from flux
        except Exception as e:                                                     # in case flux is too low and PCM_LBL crashed
            Tsurf[0,i] = np.nan
            flux[0,i] = np.nan
            axis_adj[i] = np.nan
    
    ax2.plot(axis, Tsurf[0,:],label={label},color=col,linestyle=line)
    secax2 = ax2.secondary_xaxis('top', functions=(axis_to_flux, flux_to_axis))    # add second x axis for flux
    secax2.tick_params(axis='x', labelsize=11, pad=5)
    secax2.set_xticks([150, 300, 600, 1200])

ax2.grid(True, which='both')
ax2.legend(loc='best')
ax2.xaxis.set_major_formatter(formatter)
ax2.xaxis.offsetText.set_horizontalalignment('right')
ax2.set_xlabel('Semi Major Axis (au)',fontsize=13)
secax2.set_xlabel(r'Flux (W/m$^2$)', fontsize=13, labelpad=10)
ax1.tick_params(labelsize=12)
ax2.tick_params(labelsize=12)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('aaa_surface_temperatures_1bar_20bar_he_h2_varied_conc_combined_pap.png',dpi=750)
plt.show()


