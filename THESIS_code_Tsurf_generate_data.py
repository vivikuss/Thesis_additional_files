import numpy as np
import os
import subprocess
import f90nml
from tqdm import tqdm

# create grid
au_unit = 1.5e11        # m
Lsun_unit = 3.846e26    # Watts
grid_size = 10          # number of data points

### CUSTOMIZE IF NEEDED ###
# stellar luminosity and semi major axis range / flux range
axis_si = np.linspace(0.15,0.65,grid_size)*au_unit  # in meters
lum_si = np.ones_like(axis_si)*0.0234*Lsun_unit     # in Watts
x,y = np.meshgrid(axis_si,lum_si)
co2 = [0.01, 0.1, 0.95, 0.999]                  # co2 concentrations
h = [0.99, 0.9, 0.05, 0.001]                      # He or H2 concentrations
gas = ['He_', 'H2_']                            # He or H2 atmosphere
strings = ['1p','10p','95p','999p']                 # labels for path
### 

### ADJUST THIS PART ###
# paths
exp_dir = '/Users/new/Desktop/THESIS/THESIS_PCM_LBL/example_run'
exec_name = 'PCM_LBL.e'
nml_path = '/Users/new/Desktop/THESIS/THESIS_PCM_LBL/example_run/input.nml'
results_path = "results_Tsurf_20bar_"
###

flux = np.zeros((grid_size,grid_size))

for j,g in enumerate(gas):
    for k,s in enumerate(strings):
        with open(nml_path) as nml_file_in:
            nml = f90nml.read(nml_file_in)              # open namelist file
            h_value = h[k]              
            co2_value = co2[k]
            gas_name = gas[j]
            nml['composition_nml']['gas_name_max'] = [str(gas_name), 'CO2', 'CH4', 'H2O']  # set atmosphere composition
            nml['composition_nml']['gas_molarconc_max'] = [h_value, co2_value, 0.0, -1.0]   # set concentrations
            nml_file_out = exp_dir + 'input.nml' 
            f90nml.write(nml, nml_file_out, force=True)         # overwrite former composition and concentrations
        for i in tqdm(range(grid_size)):                            # loop over different flux 
                flux_temp = lum_si[0]/(4*np.pi*axis_si[i]**2)   
                while(np.any(flux == round(flux_temp,2))):         # if luminosity isn't fixed, make sure that same flux isn't chosen twice
                    flux_temp += 0.1
                flux[0,i] = round(flux_temp,2)                  # round
                flux_label = round(flux_temp,2) 

        # print(np.max(flux), np.min(flux))
        # print(flux[0,:])

                with open(nml_path) as nml_file_in:
                    nml = f90nml.read(nml_file_in)              # open namelist file

                    nml['shortwave_nml']['Fstel0'] = flux[0,i]      # set flux
                    nml_file_out = exp_dir + 'input.nml' 
                    f90nml.write(nml, nml_file_out, force=True)         # overwrite former flux

                os.chdir(exp_dir)                                   # execute PCM_LBL for this flux
                subprocess.run(["make", "all"], check=True)
                orig_name = 'PCM_LBL.e'
                new_name = exp_dir + exec_name
                os.rename(orig_name, new_name)
                subprocess.run('./PCM_LBL.e')

                orig_name = 'results'                                   
                exp_name = results_path + f"{g}_{s}_{flux_label}"       # save data using initial flux as label
                os.rename(orig_name, exp_name)
                print("Directory '% s' created" % exp_name)
