# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:05:33 2024

@author: ryanw
"""

defined_systems = ['apep', 'WR48a', 'WR104', 'WR112', 'WR125', 'WR137', 'WR140']

def print_systems():
    ''' Prints the pre-defined WR CWB systems.
    '''
    print(defined_systems)

template_system = {"m1":22.,                    # body 1 mass (solar masses)
        "m2":10.,                               # body 2 mass
        "eccentricity":0.5,                     # orbital eccentricity
        "inclination":60.,                      # orbit inclination (degrees)
        "asc_node":254.1,                       # orbital ascending node (degrees)
        "arg_peri":10.6,                        # orbital argument of periastron (degrees)
        "open_angle":40.,                       # shock cone full opening angle (degrees)
        "period":1.,                            # orbital period (years)
        "distance":10.,                         # distance to the system (pc)
        "windspeed1":0.1,                       # expansion speed of the dust cloud (km/s)
        "windspeed2":2400.,                     # currently unused param (km/s)
        "turn_on":-180.,                        # true anomaly of dust turn on (degrees)
        "turn_off":180.,                        # true anomaly of dust turn off (degrees)
        "gradual_turn":5.,                      # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,                            # oblateness param of shock cone (currently unused)
        "nuc_dist":0.0001, "opt_thin_dist":2.,                  # nucleation and optically thin distance (AU)
        'term_windspeed':0.1, 'accel_rate':-5,                  # terminal velocity of the dust expansion (km/s) and nonparameterised acceleration rate
        "orb_sd":0., "orb_amp":0., "orb_min":180.,              # orbital dust variation: standard deviation (deg), amplitude, true anomaly of minimum (deg - 180 = periastron)
        "az_sd":30., "az_amp":0., "az_min":270.,                # azimuthal dust variation: standard deviation (deg), amplitude, angle of minimum (deg - 90 = leading edge)
        "comp_incl":127.1, "comp_az":116.5, "comp_open":0., "comp_reduction":0.,        # tertiary companion properties: inclination w.r.t. binary barycentre (deg), azimuthal position (deg), plume full opening angle (deg), amplitude of dust mass reduction
        "comp_plume":1., "comp_plume_sd":0., "comp_plume_max":0.,                       # tertiary cavity plume params (unused)
        "phase":0.6,                            # current orbital phase of the system
        "sigma":1.5,                            # sigma for gaussian blur (pixels)
        "histmax":1., "lum_power":1.,           # post processing on the image: histmax moves the maximum brightness of all pixels down, lum_power scales the luminosity of the pixels by a power law
        "spin_inc":0., "spin_Omega":0.,         # spin inclination and spin-axis offset of a star with anisotropic wind 
        "windspeed_polar":2400, "aniso_vel_mult":-6.2, "aniso_vel_power":3.53,          # velocity profile of the anisotropic wind w.r.t. latitude. polar windspeed (km/s), vel mult and vel power describe the scaling of the assumed tanh function
        "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,          # analogue for mass loss profile of anisotropic wind w.r.t. latitude. the shock full opening angle from the polar wind (deg), mult and power describe the scaling of the assumed tanh function
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1.,                     # brightness and widths of the stellar sprites for use in imaging (log scale based on the image resolution and brightness), for the first and second stars
        'star3amp':0., 'star3sd':-1., 'star3dist':0.,                                   # assuming a third star in the system, these are imaging properties of it. star3dist is the radial distance of the 3rd star from the binary barycentre (au)
        'star1lum':5.97, 'star1temp':57000, 'star2lum':5.699, 'star2temp':36000,        # for use in MCFOST: the luminosity (log10 solar lumins) and temperature (K) of each star in the binary
        'star3lum':0, 'star3temp':0,                                                    # as above, but for a third star (if there is one, i.e. if star3dist != 0)
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  # for use in MCFOST: minimum and maximum dust grain size (micron) and and whether or not to simulate dust grain size evolution   
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,              # for use in MCFOST: the dust grain evolution parameters for the surge function. 
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-10}              # for use in MCFOST: the shell dust mass max_val (solar masses) is for *each point* in the point cloud. This assumes MCFOST is using a 1:100 dust:gas mass ratio, so the actual mass will be multiplied by 100. That is, the user-entered mass here is just for the dust.                                                 
'''Template System'''

# below are rough params for Apep 
apep = {"m1":15.,                # solar masses
        "m2":10.,                # solar masses
        "eccentricity":0.82, 
        "inclination":23.8,      # degrees
        "asc_node":164.1,        # degrees
        "arg_peri":10.6,         # degrees
        "open_angle":126.,       # degrees (full opening angle)
        "period":193.,           # years
        "distance":2400.,        # pc
        "windspeed1":1024.,       # km/s
        "windspeed2":2400.,      # km/s
        "turn_on":-108.,         # true anomaly (degrees)
        "turn_off":141.,         # true anomaly (degrees)
        "gradual_turn":0.1,       # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,
        "nuc_dist":1., "opt_thin_dist":2.,           # nucleation and optically thin distance (AU)
        'term_windspeed':860, 'accel_rate':-5.,
        "orb_sd":0., "orb_amp":0., "orb_min":180., "az_sd":30., "az_amp":0.5, "az_min":90.,
        "comp_incl":124., "comp_az":238.8, "comp_open":90., "comp_reduction":1.75, "comp_plume":1.,
        "comp_plume_sd":20., "comp_plume_max":373.,
        "phase":0.35, 
        "sigma":2.,              # sigma for gaussian blur
        "histmax":1., "lum_power":1, 
        "spin_inc":0., "spin_Omega":0.,
        "windspeed_polar":2400, "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0.7, 'star1sd':-0.7, 'star2amp':0.7, 'star2sd':-0.7, 'star3amp':0.7, 'star3sd':-1.12, 'star3dist':1700.,
        'star1lum':5.34, 'star1temp':70000, 'star2lum':5.3, 'star2temp':85000, 'star3lum':5.9, 'star3temp':28000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':4e-11}
'''Apep'''
def apep_refs():
        for ref in ["White et al. 2025 - in prep.", "Han et al. 2025 - in prep", "Han et al. 2020 - 2020MNRAS.498.5604H", 
                    "Callingham et al. 2020 - 2020MNRAS.495.3323C", "Star temps/lums: Crowther 2007 - 2007ARA&A..45..177C and Ramiaramanantsoa et al 2018 - 2018MNRAS.480..972R"]:
                print(ref)

# below are rough params for WR 48a
WR48a = {"m1":15.,                  # solar masses
        "m2":10.,                   # solar masses
        "eccentricity":0.74, 
        "inclination":74.,           # degrees
        "asc_node":174.,               # degrees
        "arg_peri":124.,              # degrees
        "open_angle":37.,           # degrees (full opening angle)
        "period":32.5,              # years
        "distance":4000.,            # pc
        "windspeed1":1700.,           # km/s
        "windspeed2":900.,          # km/s
        "turn_on":-121.,             # true anomaly (degrees)
        "turn_off":137.,             # true anomaly (degrees)
        "gradual_turn":19.,
        "oblate":0.,
        "nuc_dist":0.1, "opt_thin_dist":0.2,           # nucleation and optically thin distance (AU)
        'term_windspeed':1700., 'accel_rate':-5.,
        "orb_sd":40., "orb_amp":0., "orb_min":180., "az_sd":45., "az_amp":0., "az_min":90.,
        "comp_incl":0, "comp_az":0., "comp_open":0., "comp_reduction":0., "comp_plume":0.,
        "comp_plume_sd":0., "comp_plume_max":0.,
        "phase":0.78, 
        "sigma":2,                  # sigma for gaussian blur
        "histmax":0.3, "lum_power":1., 
        "spin_inc":0., "spin_Omega":0., 
        "windspeed_polar":2400., "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.,
        'star1lum':5.5, 'star1temp':40000, 'star2lum':5.5, 'star2temp':20000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':5e-11}
'''WR48a'''
# WR48a2 = {"m1":15.,                  # solar masses
#         "m2":10.,                   # solar masses
#         "eccentricity":0.7, 
#         "inclination":81.,           # degrees
#         "asc_node":308.,               # degrees
#         "arg_peri":307.,              # degrees
#         "open_angle":27.,           # degrees (full opening angle)
#         "period":32.5,              # years
#         "distance":4000.,            # pc
#         "windspeed1":1700.,           # km/s
#         "windspeed2":900.,          # km/s
#         "turn_on":-104.,             # true anomaly (degrees)
#         "turn_off":130.,             # true anomaly (degrees)
#         "gradual_turn":23.8,
#         "oblate":0.,
#         "nuc_dist":0.1, "opt_thin_dist":0.2,           # nucleation and optically thin distance (AU)
#         'term_windspeed':1700., 'accel_rate':-5.,
#         "orb_sd":40., "orb_amp":0., "orb_min":180, "az_sd":45., "az_amp":0.3, "az_min":90,
#         "comp_incl":0, "comp_az":0, "comp_open":0, "comp_reduction":0., "comp_plume":0,
#         "comp_plume_sd":0., "comp_plume_max":0.,
#         "phase":0.78, 
#         "sigma":2.,                  # sigma for gaussian blur
#         "histmax":0.3, "lum_power":1., 
#         "spin_inc":0., "spin_Omega":0., 
#         "windspeed_polar":2400., "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
#         'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.}

# below are rough params for WR 104
WR104 = {"m1":10.,                # solar masses
        "m2":20.,                # solar masses
        "eccentricity":0.06, 
        "inclination":180.-15.,       # degrees
        "asc_node":90.,         # degrees
        "arg_peri":0.,           # degrees
        "open_angle":60.,       # degrees (full opening angle)
        "period":241.5/365.25,           # years
        "distance":2580.,        # pc
        "windspeed1":1200.,       # km/s
        "windspeed2":2000.,      # km/s
        "turn_on":-180.,         # true anomaly (degrees)
        "turn_off":180.,         # true anomaly (degrees)
        "gradual_turn":0.1,       # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,
        "nuc_dist":1., "opt_thin_dist":2.,           # nucleation and optically thin distance (AU)
        'term_windspeed':1200., 'accel_rate':-5.,
        "orb_sd":0., "orb_amp":0., "orb_min":180., "az_sd":0., "az_amp":0., "az_min":90., 
        "comp_incl":0, "comp_az":0., "comp_open":0., "comp_reduction":0., "comp_plume":0.,
        "comp_plume_sd":0., "comp_plume_max":0.,
        "phase":0.7, 
        "sigma":6.,              # sigma for gaussian blur
        "histmax":0.2, "lum_power":1., 
        "spin_inc":0., "spin_Omega":0., 
        "windspeed_polar":2400., "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.,
        'star1lum':5.5, 'star1temp':45000, 'star2lum':5, 'star2temp':20000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-13}
'''WR104'''
# below are rough params for WR 112
WR112 = {"m1":15.,                # solar masses
        "m2":10.,                # solar masses
        "eccentricity":0., 
        "inclination":100.,       # degrees
        "asc_node":360.-75.,         # degrees
        "arg_peri":170.,           # degrees
        "open_angle":110.,       # degrees (full opening angle)
        "period":19.,           # years
        "distance":2400.,        # pc
        "windspeed1":700.,       # km/s
        "windspeed2":2400.,      # km/s
        "turn_on":-180.,         # true anomaly (degrees)
        "turn_off":180.,         # true anomaly (degrees)
        "gradual_turn":5.,       # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,
        "nuc_dist":0.1, "opt_thin_dist":0.2,           # nucleation and optically thin distance (AU)
        'term_windspeed':700., 'accel_rate':-5.,
        "orb_sd":0., "orb_amp":0., "orb_min":180, "az_sd":0., "az_amp":0., "az_min":90, 
        "comp_incl":0., "comp_az":0., "comp_open":0., "comp_reduction":0., "comp_plume":0,
        "comp_plume_sd":0., "comp_plume_max":0.,
        "phase":0.6, 
        "sigma":2.,              # sigma for gaussian blur
        "histmax":0.03, "lum_power":1.3, 
        "spin_inc":0., "spin_Omega":0.,
        "windspeed_polar":2400., "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.,
        'star1lum':5.5, 'star1temp':45000, 'star2lum':5, 'star2temp':20000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-13}
'''WR112'''
def WR112_refs():
        ''''''
        for ref in ["Lau et al. 2020 - 2020ApJ...900..190L"]:
                print(ref)

# below are rough params for WR 112
WR125 = {"m1":15.,                # solar masses
        "m2":10.,                # solar masses
        "eccentricity":0.29, 
        "inclination":87.,       # degrees
        "asc_node":233.,         # degrees
        "arg_peri":175.,           # degrees
        "open_angle":35.,       # degrees (full opening angle)
        "period":28.12,           # years
        "distance":2400.,        # pc
        "windspeed1":2700.,       # km/s
        "windspeed2":2400.,      # km/s
        "turn_on":-82.,         # true anomaly (degrees)
        "turn_off":111.,         # true anomaly (degrees)
        "gradual_turn":1.,       # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,
        "nuc_dist":0.1, "opt_thin_dist":0.2,           # nucleation and optically thin distance (AU)
        'term_windspeed':2700., 'accel_rate':-5.,
        "orb_sd":0., "orb_amp":0., "orb_min":180, "az_sd":0., "az_amp":0., "az_min":90, 
        "comp_incl":0, "comp_az":0., "comp_open":0., "comp_reduction":0., "comp_plume":0,
        "comp_plume_sd":0., "comp_plume_max":0.,
        "phase":0.6, 
        "sigma":2.,              # sigma for gaussian blur
        "histmax":0.18, "lum_power":1.3, 
        "spin_inc":0., "spin_Omega":0., 
        "windspeed_polar":2400, "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.,
        'star1lum':5.5, 'star1temp':45000, 'star2lum':5, 'star2temp':20000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-13}
'''WR125'''

# below are rough params for WR 137
WR137 = {"m1":10.,                # solar masses
        "m2":20.,                # solar masses
        "eccentricity":0.315, 
        "inclination":97.2,       # degrees
        "asc_node":117.91,         # degrees
        "arg_peri":0.6,           # degrees
        "open_angle":37.2,       # degrees (full opening angle)
        "period":13.1,           # years
        "distance":1941.,        # pc
        "windspeed1":1700.,       # km/s
        "windspeed2":2000.,      # km/s
        "turn_on":-180.,         # true anomaly (degrees)
        "turn_off":180.,         # true anomaly (degrees)
        "gradual_turn":0.,       # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,
        "nuc_dist":1., "opt_thin_dist":2.,           # nucleation and optically thin distance (AU)
        'term_windspeed':1700., 'accel_rate':-5.,
        "orb_sd":0., "orb_amp":0., "orb_min":180, "az_sd":0., "az_amp":0., "az_min":90., 
        "comp_incl":0., "comp_az":0., "comp_open":0., "comp_reduction":0., "comp_plume":0.,
        "comp_plume_sd":0., "comp_plume_max":0.,
        "phase":0.9, 
        "sigma":3.,              # sigma for gaussian blur
        "histmax":1., "lum_power":1., 
        "spin_inc":0., "spin_Omega":0., 
        "windspeed_polar":2400., "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.,
        'star1lum':5.6, 'star1temp':60000, 'star2lum':5.2, 'star2temp':32000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-13}
'''WR137'''
def WR137_refs():
        ''''''
        for ref in ["Richardson et al. 2024 - 2024ApJ...977...78R", "Star lums: St-Louis et al 2020 - 2020MNRAS.497.4448S, Star Temps: Richardson et al 2016 - 2016MNRAS.461.4115R"]:
                print(ref)

WR137alt = {'m1': 9.5, 
        'm2': 17.3, 
        'eccentricity': 0.315, 
        'inclination': 97.2, 
        'asc_node': 155.0, 
        'arg_peri': 1.0, 
        'open_angle': 24.0, 
        'period': 13.1, 
        'distance': 2040.0, 
        'windspeed1': 1700.0, 
        'windspeed2': 1700.0, 
        'turn_on': -159.0, 
        'turn_off': 85.0, 
        'gradual_turn': 2.6, 
        'oblate': 0.0, 'nuc_dist': 0.1, 'opt_thin_dist': 2.0, 
        'term_windspeed': 1700.0, 'accel_rate': -5.0, 
        'orb_sd': 53.0, 'orb_amp': 1.0, 'orb_min': 322.9, 'az_sd': 5.3, 'az_amp': -0.88, 'az_min': 21.2, 
        'comp_incl': 0.0, 'comp_az': 0.0, 'comp_open': 0.0, 'comp_reduction': 0.0, 'comp_plume': 0.0, 
        'comp_plume_sd': 0.0, 'comp_plume_max': 0.0, 
        'phase': 0.16, 
        'sigma': 3.24, 
        'histmax': 1.0, 'lum_power': 0.47, 
        'spin_inc': 0.0, 'spin_Omega': 0.0, 
        'windspeed_polar': 1700.0, 'aniso_vel_mult': -6.30, 'aniso_vel_power': 1.99, 'open_angle_polar': 0.0, 'aniso_OA_mult': -5.30, 'aniso_OA_power': 3.53, 
        'star1amp': 1.0, 'star1sd': -0.588, 'star2amp': 2.520, 'star2sd': -3.0, 'star3amp': 0.0, 'star3sd': -1.0, 'star3dist': 0.0,
        'star1lum':5.6, 'star1temp':60000, 'star2lum':5.2, 'star2temp':32000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-13}

# below are rough params for WR 140
WR140 = {"m1":8.4,                # solar masses
        "m2":20.,                # solar masses
        "eccentricity":0.8964, 
        "inclination":119.6,       # degrees
        "asc_node":275.,         # degrees
        "arg_peri":180.-46.8,           # degrees
        "open_angle":80.,       # degrees (full opening angle)
        "period":2896.35/365.25,           # years
        "distance":1670.,        # pc
        "windspeed1":2600.,       # km/s
        "windspeed2":2400.,      # km/s
        "turn_on":-135.,         # true anomaly (degrees)
        "turn_off":135.,         # true anomaly (degrees)
        "gradual_turn":0.5,       # gradual turn off/on (deg) -- standard deviation of gaussian fall off
        "oblate":0.,
        "nuc_dist":50., "opt_thin_dist":220.,           # nucleation and optically thin distance (AU)
        'term_windspeed':2600., 'accel_rate':-5.,
        "orb_sd":80., "orb_amp":0., "orb_min":180., "az_sd":60., "az_amp":0., "az_min":90.,
        "comp_incl":0., "comp_az":0., "comp_open":0., "comp_reduction":0., "comp_plume":0.,
        "comp_plume_sd":0., "comp_plume_max":0.,
        "phase":0.6, 
        "sigma":2.,              # sigma for gaussian blur
        "histmax":1., "lum_power":1., 
        "spin_inc":0., "spin_Omega":0.,
        "windspeed_polar":240.0, "aniso_vel_mult":-6.2, "aniso_vel_power":3.53, "open_angle_polar":180., "aniso_OA_mult":-6.05, "aniso_OA_power":3.53,
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.,
        'star1lum':5.97, 'star1temp':57000, 'star2lum':5.699, 'star2temp':36000,
        'amin':0.001, 'amax':0.5, 'dust_grain_beta':1,                                  
        'dust_grain_b':5, 'dust_grain_c':0.05, 'dust_grain_max_val':2, 'dust_grain_d':0.2,
        'dust_mass_beta':1, 'dust_mass_b':5, 'dust_mass_c':0.1, 'dust_mass_max_val':1e-13}
'''WR140'''
def WR140_refs():
        ''''''
        for ref in ["Han et al. 2022 - 2022Natur.610..269H", "Lau et al. 2022 - 2022NatAs...6.1308L"]:
                print(ref)


