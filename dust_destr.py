import numpy as np

M_odot = 1.98e30
yr_2_s = 365 * 24 * 60**2
au_2_m = 1.96e11

### --- Sublimation Distance --- ###
L_uv = 10**5
T_sub = 1800
pc_to_AU = 206265

sub_distance = 0.015 * (L_uv / 10**9)**0.5 * (T_sub / 1800)**(-5.6/2) * pc_to_AU
print("Sublimation distance =", sub_distance, "au")


### --- Shock Open Angle Analysis --- ###
expect_ratio = (121 / (90/2) - 31/90)**3

calc_ratio = 10**-4 * 860 / (10**-5.2 * 1280)

print(expect_ratio, calc_ratio)



### --- RATD disruption time --- ###
temperature = 30000
mean_lambda = 4107 / temperature    # 50th percentile of planck function (in microns)
luminosity = 10**5.9    # solar lumins
grain_size = 40        # angstroms
dist = 1700             # dust distance, au
tens_str = 2e10          # dust tensile strength

# disr_timescale = 1.6 * (mean_lambda / 0.11)**1.7 * (1.43 * 10**6 / luminosity) * (grain_size / 500)**-0.7 * (dist / 1650)**2 * (tens_str / 10**9)**0.5
# print("RATD disruption timescale =", disr_timescale, "days")
# crit_grain_size = 84 * ((1.43 * 10**6 / luminosity)**3 * (dist / 1650)**(2/3) * (mean_lambda / 0.11)**1.7 * (tens_str / 10**9)**0.5)**(1/2.7)
# print("Critical grain size =", crit_grain_size, "A")

crit_grain_size = 0.003197 * ((mean_lambda / 0.5)**-1.7 * (luminosity / (10**9 * (dist / pc_to_AU)**2))**(-1/3) * (tens_str / 10**9)**1/2)**(1/2.7)

disr_time = (368/365) * (mean_lambda / 0.5)**-1.7 * (10 * crit_grain_size)**-0.7 * (luminosity * 1.2 / (10**9 * (dist / pc_to_AU)**2))**-1 * (tens_str / 10**9)**0.5
print("Critical grain size =", crit_grain_size, "micron =", crit_grain_size * 10**4, "A")
print("RATD disruption timescale =", disr_time, "yr")



# ### --- Grain-grain collisions --- ###
# gas_to_dust_r = 100             # gas to dust ratio
# hydrogen_mass = 1.67e-27        # kg
# grain_size = 40e-10            # m
# density = 1.6 * 100**3 / 1e3    # kg/m^3
# density = 10**-5 * M_odot / (4 * np.pi * (dist * au_2_m)**2 * 860e3 * yr_2_s)
# # print(density * 1e3 / 1e6)
# hydrogen_windspeed = 1280e3     # m/s
# hydrogen_mass_loss = 10**-5.2 * M_odot / yr_2_s     # kg/s
# hydrogen_number_density = ((hydrogen_mass_loss / hydrogen_mass) / hydrogen_windspeed) / (4 * np.pi * (dist * au_2_m)**2)
# print(hydrogen_number_density)
# drift_velocity = hydrogen_windspeed + 860e3
# drift_velocity = 30e3

# grain_grain_timescale = 4 * density * grain_size * gas_to_dust_r / (3 * hydrogen_number_density * hydrogen_mass * drift_velocity) / yr_2_s

# # grain_grain_timescale = (np.pi * grain_size**2 * (density / (1e2 * hydrogen_mass)) * drift_velocity)**-1  / yr_2_s
# print(f"grain-grain timescale: {grain_grain_timescale} yr")