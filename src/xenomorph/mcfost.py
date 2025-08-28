'''
Various functions to make the communication between xenomorph and MCFOST a bit easier. These are broadly written with running on a HPC-cluster in mind.
'''
import jax.numpy as jnp
import numpy as np
import io
from astropy.io import fits
import matplotlib.pyplot as plt
import os
import gzip
import shutil
import itertools

import src.xenomorph.geometry as gm
import src.xenomorph.systems as wrb

stef_boltz = 5.670374419e-8     # W/m^2/K^4
solar_radius = 696340000        # m
solar_lum = 3.83e+26             # W

# filter transmittances gotten from https://irtfweb.ifa.hawaii.edu/~nsfcam2/Filter_Profiles.html
H_band_samples = {1.45 : 0.0715157, 1.5328 : 0.662124, 1.56397 : 0.652174, 1.634 : 0.687081, 1.7 : 0.637728, 1.78 : 0.05}
for wavelength in H_band_samples:
    H_band_samples[wavelength] *= 1.2464    # the transmittances used above are for the blocked H filter, so need to multiply all the transmittance vals
K_band_samples = {1.9654 : 0.049453, 2.079 : 0.798509, 2.1645 : 0.803215, 2.3 : 0.766, 2.3708 : 0.75372, 2.457 : 0.016607}
L_band_samples = {3.1309 : 0.01, 3.23 : 0.921975, 3.7037 : 0.925085, 3.751 : 0.9036, 3.89408 : 0.0108354}
M_band_samples = {4.4484 : 0.010919, 4.6 : 0.81075, 4.708 : 0.840764, 4.8828 : 0.90181, 5.0454 : 0.79153, 5.11247 : 0.86137, 5.27426 : 0.010345}

bandpasses = {'H': H_band_samples, 'K': K_band_samples, 'L': L_band_samples, 'M': M_band_samples}
# band 0-mag fluxes here? https://about.ifa.hawaii.edu/ukirt/calibration-and-standards/astronomical-utilities/zero-mag-fluxes-and-conversions/
zero_points = {'H': 1.18e-09, 'K': 4e-10, 'L': 7.3e-11, 'M': 2.12e-11}



def trapezoid_rule(x1, x2, y1, y2):
    ''' Calculates the area of the trapezoid made by two points.
    Parameters
    ----------
    x1, x2 : float
        The left and right x positions
    y1, y2 : float
        The left and right y positions
    Returns
    -------
    float
        The area of the trapezoid in units of x*y
    '''
    return 0.5 * abs(x2 - x1) * (y1 + y2)

def filter_bandpasses(filter):
    ''' WIP
    - Filter bandpasses (H,K,L,M) are available at https://irtfweb.ifa.hawaii.edu/~nsfcam2/Filter_Profiles.html
    Parameters
    ----------
    filter : str
        One of {'H', 'K', 'L', 'M'} corresponding to the filter bandpass wanted. The 'J' band is omitted as it usually can't pick up dust formation. 
    Returns
    -------
    bandpass : dict
        A dictionary where the keys are the wavelength samples and the vals are the transmittances at that wavelength
    '''
    return bandpasses[filter]


def mcfost_points(stardata, shells, filename, n_t=1000, n_points=400, resolution=600, root_dir=''):
    ''' Generates points that can be fed into a new version of MCFOST for radiative transfer calculations.
    Once generated, you could use these points with MCFOST via:

    mcfost <system>.para -df <filename> -force_Mgas -fix_star -star_bb
    mcfost <system>.para -df <filename> -force_Mgas -fix_star -star_bb -img 1.6
    
    Parameters
    ----------
    stardata : dict
        The system parameter file.
    shells : int
        The number of shells to generate.
    filename : str
        The name of the file to save the points into. This *must* include a '.fits' suffix.
    n_t : int
        The number of rings to generate in each shell.
    n_points : int
        The number of points to generate in each ring.
    resolution : int
        The number of pixels (per side) for the geometric comparison image.
    root_dir : str
        The directory where you'd like the output of the job to be.
    '''
    if root_dir != '':
        save_dir = root_dir + '/'
    else:
        save_dir = root_dir
    
    stardatacopy = stardata.copy()
    stardatacopy['sigma'] = 0.5
    particles, weights = gm.dust_plume_custom(stardatacopy, shells, n_t=n_t, n_points=n_points)

    # make an image of what we expect from the stock geometric model so we can compare with the radiative transfer output
    fig, ax = plt.subplots()
    xbound, ybound = jnp.max(jnp.abs(particles[0, :])), jnp.max(jnp.abs(particles[1, :]))
    bound = jnp.max(jnp.array([xbound, ybound])) * (1. + 2. / resolution)
    pixel_bins = jnp.linspace(-bound, bound, resolution+1)
    X, Y, H = gm.smooth_histogram2d_w_bins(particles, weights, stardatacopy, pixel_bins, pixel_bins)
    ax.pcolormesh(-X, Y, H, cmap='hot', rasterized=True)
    ax.set(aspect='equal', ylabel='Relative Dec (")', xlabel='Relative RA (")')
    ax.invert_xaxis()
    fig.savefig(save_dir + f'{filename[:-5]}_geometric_model.png', dpi=300, bbox_inches='tight')
    plt.close('all')


    particles = jnp.tan(particles / (60 * 60 * 180 / jnp.pi)) * (stardatacopy['distance'] * 3.086e13) # convert from angular coords back to physical coords
    particles /= gm.AU2km  # MCFOST needs distances in au

    # get rid of any points that have no mass
    filter = np.where(weights > 0)[0]
    particles = particles[:, filter]
    weights = weights[filter]

    # assign masses to each point
    masses = 1e2 * stardata['dust_mass'] * shells * weights / jnp.sum(weights)     # the 1e2 factor assumes a 1:100 dust:gas mass ratio, and these are actually the gas masses
    
    # particles += np.random.normal(0, 5e-2, size=(3, len(weights)))    # add small random offsets to the particles (in au) to stop the tesselation from crashing (strange bug with mcfost!)
    particles *= np.random.normal(1, 1e-3, size=(3, len(weights)))    # add small random offsets to the particles (in au) to stop the tesselation from crashing (strange bug with mcfost/voro++!)

    fits_masses = fits.PrimaryHDU(masses)
    fits_positions = fits.ImageHDU(particles.T)     # transposed to get the orientation right (although it doesnt affect the calc at all)
    hdul = fits.HDUList([fits_masses, fits_positions])
    hdul.writeto(save_dir + filename, overwrite=True)

    



def generate_para(stardata, paraname, density_file, photons=1e7, T_photons=1e7, resolution=600, gas_2_dust=100, root_dir=''):
    '''WIP -- Generates a .para file to be used in the MCFOST run. 
    Note:
     - The dust mass *must* be set at run time (through the density_file provided)
    Assumes:
     - Amorphous carbon dust
     - Each star is effectively right in the centre of the dust cloud (well within 5au of the centre)
    Todo:
     - specify the grain distribution in of the dust
    Parameters
    ----------
    stardata : dict
        The system parameter file.
    paraname : str
        The name that you'd like to give to this parameter file. A '.para' is automatically appended to the end of this input.
    density_file : str
        The name of the .fits file generated by `xmc.mcfost_points()`. 
    photons : int
        The number of photons to use in the imaging computation.
    T_photons : int
        The number of photons to use in the T computation
    resolution : int
        The pixel side length of the computed image.
    gas_2_dust : float 
        The mass of gas relative to the dust in each particle
    root_dir : str
        The directory where you'd like the output of the job to be.
    '''
    if root_dir != '':
        write_dir = f'{root_dir}/'
    else:
        write_dir = ''
    # first, let's start by calculating our (physical) image size (in au) from the given density file 
    data = fits.open(write_dir + density_file)
    particles = data[1].data
    particles = np.abs(particles)
    img_bound = 1.05 * 2 * np.max(particles[:, :2]) # want it slightly bigger than twice the radius from the origin, in the projection of the sky (hence the :2 slice)

    parafile = io.open(f'{write_dir + paraname}.para', 'w', newline='\n')

    parafile.write("4.1                      mcfost version\n\n"+\
                    "#Number of photon packages\n"+\
                    f"  {T_photons:.2e}                  nbr_photons_eq_th  : T computation\n"+\
                    "  1.28e3	          nbr_photons_lambda : SED computation\n"+\
                    f"  {photons:.2e}                  nbr_photons_image  : images computation\n\n")
    parafile.write("#Wavelength\n"+\
                    "  100  0.02 3000.0          n_lambda, lambda_min, lambda_max [mum] Do not change this line unless you know what you are doing\n"+\
                    "  T F T 		  compute temperature?, compute sed?, use default wavelength grid for output ?\n"+\
                    "  IMLup.lambda		  wavelength file (if previous parameter is F)\n"+\
                    "  F F			  separation of different contributions?, stokes parameters?\n\n")
    parafile.write("#Grid geometry and size\n"+\
                    "  2			  1 = cylindrical, 2 = spherical (a Voronoi mesh is selected automatically with -phantom)\n"+\
                    " 100 70 1 20              n_rad (log distribution), nz (or n_theta), n_az, n_rad_in\n\n")
    parafile.write("#Maps\n"+\
                    f"  {resolution} {resolution} {int(img_bound)}.            grid (nx,ny), size [AU]\n"+\
                    "  0.  0.  1  F           RT: imin, imax, n_incl, centered ?\n"+\
                    "  0    0.   1             RT: az_min, az_max, n_az angles\n"+\
                    f"  {stardata['distance']:.1f}			  distance (pc)\n"+\
                    "  -90.			  disk PA\n\n")
    parafile.write("#Scattering method\n"+\
                    "  2	                  1=exact phase function, 2=hg function with same g (2 implies the loss of polarizarion)\n\n"+\
                    "#Symmetries\n"+\
                    "  F	                  image symmetry\n"+\
                    "  F	                  central symmetry\n"+\
                    "  F	                  axial symmetry (important only if N_phi > 1)\n\n")
    parafile.write("#Disk physics\n"+\
                    "  0     0.50  1.0	  dust_settling (0=no settling, 1=parametric, 2=Dubrulle, 3=Fromang), exp_strat, a_strat (for parametric settling)\n"+\
                    "  F                       dust radial migration\n"+\
                    "  F		  	  sublimate dust\n"+\
                    "  F                       hydostatic equilibrium\n"+\
                    "  F  1e-5		  viscous heating, alpha_viscosity\n\n"+\
                    "#Number of zones : 1 zone = 1 density structure + corresponding grain properties\n"+\
                    "  1                       needs to be 1 if you read a density file (phantom or fits file)\n\n")
    # in the below block, the dust mass is given from the density_file, so we only specify the gas-to-dust mass ratio
    parafile.write("#Density structure\n"+\
                    "  3                       zone type : 1 = disk, 2 = tappered-edge disk, 3 = envelope, 4 = debris disk, 5 = wall\n"+\
                    f"  1.e-15    {gas_2_dust:.1f}		  dust mass,  gas-to-dust mass ratio\n"+\
                    "  10.  100.0  2           scale height, reference radius (AU), unused for envelope, vertical profile exponent (only for debris disk)\n"+\
                    "  100.0  0.0    300.  100.  Rin, edge, Rout, Rc (AU) Rc is only used for tappered-edge & debris disks (Rout set to 8*Rc if Rout==0)\n"+\
                    "  1.125                   flaring exponent, unused for envelope\n"+\
                    "  -0.5  0.0    	          surface density exponent (or -gamma for tappered-edge disk or volume density for envelope), usually < 0, -gamma_exp (or alpha_in & alpha_out for debris disk)\n\n")
    parafile.write("#Grain properties\n"+\
                    "  1  Number of species\n"+\
                    "  Mie  1 2  0.2  1.0  0.9 Grain type (Mie or DHS), N_components, mixing rule (1 = EMT or 2 = coating),  porosity, mass fraction, Vmax (for DHS)\n"+\
                    "  ac_opct.dat  1.0  Optical indices file, volume fraction\n"+\
                    "  1	                  Heating method : 1 = RE + LTE, 2 = RE + NLTE, 3 = NRE\n"+\
                    f"  {stardata['amin']}  {stardata['amax']} {stardata['aexp']:.1f} 100 	  amin, amax [mum], aexp, n_grains (log distribution)\n\n")
    parafile.write("#Molecular RT settings\n"+\
                    "  T T T                   lpop, laccurate_pop, LTE\n"+\
                    "  0.05 km/s		  Turbulence velocity, unit km/s or cs\n"+\
                    "  1			  Number of molecules\n"+\
                    "  co.dat 6                molecular data filename, level max up to which NLTE populations are calculated\n"+\
                    "  T 1.e-4 abundance.fits.gz   cst molecule abundance ?, abundance, abundance file\n"+\
                    "  F  2                       ray tracing ?,  number of lines in ray-tracing\n"+\
                    "  2 3	 		  transition numbers\n"+\
                    "  -10.0 10.0 40     	  vmin and vmax [km/s], number of velocity bins betwen 0 and vmax\n\n")
    parafile.write("#Atoms settings / share some informations with molecules\n"+\
                    " 1		number of atoms\n"+\
                    " H_6.atom	all levels treated in details at the moment\n"+\
                    " F		non-LTE ?\n"+\
                    " 0		initial solution, 0 LTE, 1 from file\n"+\
                    " 1000 101	vmax (km/s), n_points for ray-traced images and total flux\n"+\
                    " T 1		images (T) or total flux (F) ? Number of lines for images\n"+\
                    " 3 2		upper level -> lower level (Atomic model dependent)\n\n")

    num_stars = 2 if stardata['star3dist'] == 0 else 3
    parafile.write("#Star properties\n"+\
                    f" {num_stars} Number of stars\n")
    for star in range(num_stars):
        pos = 0 if star == 0 else 1
        star_radius = jnp.sqrt(10**stardata[f'star{star+1}lum'] * solar_lum / (4 * jnp.pi * stardata[f'star{star+1}temp']**4 * stef_boltz))     # use the stefan boltzmann law to calculate stellar radius
        star_radius /= solar_radius     # convert from m to R_sun (needed for MCFOST)
        parafile.write(f" {stardata[f'star{star+1}temp']:.1f}	{star_radius:.1f}	15.0	{pos*(-1)**star}.0	{pos*(-1)**star}.0	0.0  T Temp, radius (solar radius),M (solar mass),x,y,z (AU), automatic spectrum?\n"+\
                    " lte4000-3.5.NextGen.fits.gz\n"+\
                    " 0.0	2.2  fUV, slope_fUV\n")

    parafile.close()


def generate_slurm(slurmname, wavelength, para_file, density_file, cpus=4, run_hours=4, memory=4, root_dir='', job_name="mcfost-transfer",
                   email='ryan.white1@hdr.mq.edu.au', mcfost_setup='~/setup_mcfost'):
    ''' Generates a slurm script to run a *single* radiative transfer calculation on a xenomorph-generated spiral. 
    The script will generate the temperature profile of the (currently default-only) dust, and then image it and the specified wavelength.

    Todo:
      - ?

    Parameters
    ----------
    slurmname : str
        The name that you'd like to give to this slurm script. A '.q' is automatically appended to the end of this input.
    wavelength : int or float, or str or dict
        The wavelength (in microns) that you'd like to generate the image for.
        If wavelength is a str type, it will be interpreted as one of the pre-defined filters {'H', 'K', 'L', 'M'} and representative samples will be generated from that filter.
        If wavelength is a dict, it will be as for the str case, but for user-defined wavelengths.
    para_file : str
        The name of the MCFOST parameter file for the system.
    density_file : str
        The name of the .fits file generated by `xmc.mcfost_points()`. 
    cpus : int
        The number of CPUs you'd like to allocate to running this MCFOST job. A power of 2 is usually good.
    run_hours : int
        How many (wall-time) hours you'd like to set the job to run before the scheduling system cancels it.
    memory : float or int
        The amount of memory (in GB) to allocate to the job. 
        In my experience they typically use of order a few hundred MB, so setting 1-4GB is usually safe.
    root_dir : str
        The directory where you'd like the output of the job to be. 
    job_name : str
        A name for the job (only visible on the HPC queue system).
    email : str
        The email of the user, should they want email updates on how the job is doing. Mine by default :)
    mcfost_setup : str
        The location (and name) of the mcfost_setup file. This file is meant to be read each time an MCFOST job is run on a HPC. 
        A typical ~/setup_mcfost file will look like:
            export PATH=/<path to mcfost>/mcfost/bin:${PATH}
            export MCFOST_UTILS=/<path to mcfost>/mcfost/utils 
    '''
    if root_dir != '':
        write_dir = f'{root_dir}/'
    else:
        write_dir = ''
    if email != '':
        email_lines = ["#SBATCH --mail-type=BEGIN\n", "#SBATCH --mail-type=FAIL\n", "#SBATCH --mail-type=END\n",
                      f"#SBATCH --mail-user={email}\n", '\n']
    else:
        email_lines = ['\n']

    hashed_lines = ["#!/bin/bash\n", "#SBATCH --ntasks=1\n", f"#SBATCH --cpus-per-task={cpus}\n",
                    f"#SBATCH --job-name={job_name}\n", f"#SBATCH --output={job_name + str(wavelength)}.qout\n",
                    f"#SBATCH --time=0-{run_hours}:00:00\n", f"#SBATCH --mem={memory}G\n"]
    for email_line in email_lines:
        hashed_lines.extend(email_line)

    initialise_lines = ['echo "HOSTNAME = $HOSTNAME"\n', 'echo "HOSTTYPE = $HOSTTYPE"\n',
                        'echo Time is `date`\n', 'echo Directory is `pwd`\n', '\n']
    
    environment_lines = ['ulimit -s unlimited\n', f'source {mcfost_setup}\n', f'export OMP_NUM_THREADS={cpus}\n', 
                         '\n', 'echo "Starting mcfost..."\n', '\n']

    mcfost_lines = [f'mcfost {para_file} -df {density_file} -fix_star -star_bb\n']
    if type(wavelength) == str or type(wavelength) == dict:
        wavelengths = list(bandpasses[wavelength].keys()) if type(wavelength) == str else list(wavelength.keys())
        for sample_lambda in wavelengths:
            mcfost_lines.append(f'mcfost {para_file} -df {density_file} -fix_star -star_bb -img {sample_lambda}\n')
    else:
        mcfost_lines.append(f'mcfost {para_file} -df {density_file} -fix_star -star_bb -img {wavelength}\n')

    slurmfile = io.open(f'{write_dir + slurmname}.q', 'w', newline='\n')

    slurmfile.writelines(hashed_lines)
    slurmfile.writelines(initialise_lines)
    slurmfile.writelines(environment_lines)
    slurmfile.writelines(mcfost_lines)

    slurmfile.close()

def sample_phases(method, n_samples):
    '''
    '''
    if method == 'equal':
        phase_samples = jnp.arange(0, 1, 1. / n_samples)
    else:   # must be 'periastron_dense' in this case
        # we should overhaul periastron_dense to take into account the dust turn on/off to well sample around this
        phase_samples_first_half = jnp.logspace(-3, jnp.log10(0.5), n_samples//2) 
        phase_samples_second_half = 1 - jnp.logspace(-3, jnp.log10(0.5), n_samples - n_samples//2 + 1)[:-1][::-1]
        phase_samples = jnp.append(phase_samples_first_half, phase_samples_second_half)
    
    return phase_samples

def generate_lightcurve(stardata, wavelength, method='equal', n_samples=20, shells=1, n_t=600, n_points=200, photons=2e7, T_photons=1e7, gas_2_dust=100, 
                        resolution=30, root_dir='', cpus=8, run_hours=2, memory=4, job_name="mcfost-lightcurve", email='', 
                        mcfost_setup='~/setup_mcfost'):
    '''
    Parameters
    ----------
    stardata : dict
        The system parameter file.
    wavelength : int or float, or str or dict
        The wavelength (in microns) that you'd like to generate the image for.
        If wavelength is a str type, it will be interpreted as one of the pre-defined filters {'H', 'K', 'L', 'M'} and representative samples will be generated from that filter.
        If wavelength is a dict, it will be as for the str case, but for user-defined wavelengths.
    method : str or j/np.array
        This parameter dictates how the time samples across orbital phase are distributed. If method=='equal', there will be n_samples equally spaced samples across 
        orbital phase 0 to 1 to construct the light curve. If method=='periastron_dense', there will be proportionally more samples around periastron (when there 
        is active dust production). If method is a j/np array, the values of the one-dimensional array will be used as the phase samples.
    n_samples : int
        The number of orbital phase samples with which to construct the light curve. This is only relevant if the `method` parameter is a string. 
    shells : int
        The number of shells to generate.
    n_t : int
        The number of rings to generate in each shell.
    n_points : int
        The number of points to generate in each ring.
    photons : int
        The number of photons to use in the imaging computation.
    T_photons : int
        The number of photons to use in the T computation
    gas_2_dust : float 
        The mass of gas relative to the dust in each particle
    resolution : int
        The number of pixels (per side) for the geometric comparison image.
    root_dir : str
        The directory where you'd like the output of the job to be.
    cpus : int
        The number of CPUs you'd like to allocate to running this MCFOST job. A power of 2 is usually good.
    run_hours : int
        How many (wall-time) hours you'd like to set the job to run before the scheduling system cancels it.
    memory : float or int
        The amount of memory (in GB) to allocate to the job. 
        In my experience they typically use of order a few hundred MB, so setting 1-4GB is usually safe.
    job_name : str
        A name for the job (only visible on the HPC queue system).
    email : str
        The email of the user, should they want email updates on how the job is doing. Mine by default :)
    mcfost_setup : str
        The location (and name) of the mcfost_setup file. This file is meant to be read each time an MCFOST job is run on a HPC. 
        A typical ~/setup_mcfost file will look like:
            export PATH=/<path to mcfost>/mcfost/bin:${PATH}
            export MCFOST_UTILS=/<path to mcfost>/mcfost/utils 
    '''
    if type(method) == str:
        phase_samples = sample_phases(method, n_samples)
    else:
        phase_samples = method.copy()
        n_samples = len(method)
    
    if root_dir != '':
        write_dir = f'{root_dir}/'
    else:
        write_dir = ''
    
    
    for i, phase in enumerate(phase_samples):
        phase_dir = write_dir + f'sample_{i}'
        os.makedirs(phase_dir)
        stardata_sample = stardata.copy()
        stardata_sample['phase'] = phase
        # start by creating all of the density files within sampled phase directories
        mcfost_points(stardata_sample, shells, 'densityfile.fits', n_t=n_t, n_points=n_points, resolution=resolution, root_dir=phase_dir)

        # now create the para files (doing them seperately for now in case we want to change grain size params later on)
        generate_para(stardata_sample, 'systempara', 'densityfile.fits', photons=photons, T_photons=T_photons, resolution=resolution, 
                        gas_2_dust=gas_2_dust, root_dir=phase_dir)
    
        # now finally generate all of the necessary slurm scripts
        generate_slurm(f'sample_{i}', wavelength, 'systempara.para', 'densityfile.fits', cpus=cpus, run_hours=run_hours, memory=memory, root_dir=phase_dir, 
                        job_name=f"{job_name}_{i}", email=email, mcfost_setup=mcfost_setup)
    
    # now write a bash script to queue all of the ozstar jobs
    lines = [f"for (( num=0; num<{n_samples}; num++))\n", "do\n", f" cd sample_$num\n", f" sbatch sample_$num.q\n", f" cd ..\n", "done\n"]
    bashscript = io.open(f'{write_dir}generate_lightcurve.sh', 'w', newline='\n')
    bashscript.writelines(lines)
    bashscript.close()

def lightcurve_plot(folder, wavelength, phases='equal'):
    '''
    Some help gotten from https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    Todo:
        - account for custom phase samples
    Parameters:
    -----------
    folder : str
    wavelength : 
    phases : str or j/np.array
    '''
    subdirectories = [f.name for f in os.scandir(folder) if f.is_dir()]
    n_samples = len(subdirectories)
    sample_nums = [int(subdirectory[7:]) for subdirectory in subdirectories]

    if type(phases) == str:
        phases = sample_phases(phases, n_samples)
        
    fluxes = np.zeros(n_samples)

    for i in range(n_samples):
        current_dir = folder + f'/sample_{i}/'
        if type(wavelength) == str or type(wavelength) == dict:
            if type(wavelength) == str:
                wavelengths = list(bandpasses[wavelength].keys())
                transmittances = bandpasses[wavelength].copy()
            elif type(wavelength) == dict:
                wavelengths = list(wavelength.keys())
                transmittances = wavelength.copy()

            running_flux = 0
            running_transmittance = 0

            for j, LAMBDA in enumerate(wavelengths):
                with gzip.open(current_dir + f'data_{LAMBDA}/RT.fits.gz', 'rb') as f_in:
                    with open(current_dir + f'data_{LAMBDA}/RT.fits', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            
                hdul = fits.open(current_dir + f"data_{LAMBDA}/RT.fits")
                data = hdul[0].data[0][0][0]

                integrated_flux = np.sum(data)

                if j > 0:
                    running_flux += trapezoid_rule(wavelengths[j - 1], LAMBDA, old_integrated_flux * transmittances[wavelengths[j - 1]], 
                                            integrated_flux * transmittances[LAMBDA])
                    running_transmittance += trapezoid_rule(wavelengths[j - 1], LAMBDA, transmittances[wavelengths[j - 1]], transmittances[LAMBDA])
                    
                old_integrated_flux = integrated_flux
            integrated_flux = running_flux

        elif type(wavelength) == int or type(wavelength) == float:
            with gzip.open(current_dir + f'data_{wavelength}/RT.fits.gz', 'rb') as f_in:
                    with open(current_dir + f'data_{wavelength}/RT.fits', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            hdul = fits.open(current_dir + f"data_{wavelength}/RT.fits")
            data = hdul[0].data[0][0][0]
            integrated_flux = np.sum(data)
        
        fluxes[i] = integrated_flux
    
    phases = np.append(np.append(phases - 1, phases), phases + 1)
    fluxes = np.tile(fluxes, 3)
    
    fig, ax = plt.subplots()
    ax.plot(phases, fluxes)
    ax.set(xlabel='Phase', ylabel='Flux (W/m^2)', yscale='log', xlim=(-0.05, 1.05))
    fig.savefig(folder+'/lightcurve.png', dpi=400, bbox_inches='tight')

    if type(wavelength) == str:
        mags = -2.512 * np.log10(fluxes) + 2.512 * np.log10(zero_points[wavelength])
        fig, ax = plt.subplots()
        if n_samples >= 30:
            ax.plot(phases, mags)
        else:
            ax.scatter(phases, mags)
        ax.set(xlabel='Phase', ylabel='Magnitude', xlim=(-0.05, 1.05))
        ax.invert_yaxis()
        fig.savefig(folder+'/lightcurve_mag.png', dpi=400, bbox_inches='tight')

def lightcurve_grid(stardata, wavelength, parameter_grid, method='equal', n_samples=20, shells=1, n_t=600, n_points=200, photons=2e7, T_photons=1e7, gas_2_dust=100, 
                        resolution=30, root_dir='', cpus=8, run_hours=2, memory=4, job_name="mcfost-lightcurve", email='', 
                        mcfost_setup='~/setup_mcfost'):
    '''
    stardata : dict
        The system parameter file.
    wavelength : int or float, or str or dict
        The wavelength (in microns) that you'd like to generate the image for.
        If wavelength is a str type, it will be interpreted as one of the pre-defined filters {'H', 'K', 'L', 'M'} and representative samples will be generated from that filter.
        If wavelength is a dict, it will be as for the str case, but for user-defined wavelengths.
    parameter_grid : dict
        A dictionary where each key corresponds to the parameter of `stardata` being changed. The value for that key should be an array corresponding to the different values
        which will be used to generate a light curve. Hence, there will be n_param1 * n_param2 * ... light curves generated from this.  
    method : str or j/np.array
        This parameter dictates how the time samples across orbital phase are distributed. If method=='equal', there will be n_samples equally spaced samples across 
        orbital phase 0 to 1 to construct the light curve. If method=='periastron_dense', there will be proportionally more samples around periastron (when there 
        is active dust production). If method is a j/np array, the values of the one-dimensional array will be used as the phase samples.
    n_samples : int
        The number of orbital phase samples with which to construct the light curve. This is only relevant if the `method` parameter is a string. 
    shells : int
        The number of shells to generate.
    n_t : int
        The number of rings to generate in each shell.
    n_points : int
        The number of points to generate in each ring.
    photons : int
        The number of photons to use in the imaging computation.
    T_photons : int
        The number of photons to use in the T computation
    gas_2_dust : float 
        The mass of gas relative to the dust in each particle
    resolution : int
        The number of pixels (per side) for the geometric comparison image.
    root_dir : str
        The directory where you'd like the output of the job to be.
    cpus : int
        The number of CPUs you'd like to allocate to running this MCFOST job. A power of 2 is usually good.
    run_hours : int
        How many (wall-time) hours you'd like to set the job to run before the scheduling system cancels it.
    memory : float or int
        The amount of memory (in GB) to allocate to the job. 
        In my experience they typically use of order a few hundred MB, so setting 1-4GB is usually safe.
    job_name : str
        A name for the job (only visible on the HPC queue system).
    email : str
        The email of the user, should they want email updates on how the job is doing. Mine by default :)
    mcfost_setup : str
        The location (and name) of the mcfost_setup file. This file is meant to be read each time an MCFOST job is run on a HPC. 
        A typical ~/setup_mcfost file will look like:
            export PATH=/<path to mcfost>/mcfost/bin:${PATH}
            export MCFOST_UTILS=/<path to mcfost>/mcfost/utils 
    '''
    if root_dir != '':
        write_dir = f'{root_dir}/'
    else:
        write_dir = ''
        
    parameters = list(parameter_grid.keys())
    n_params = len(parameters)

    param_ranges = [parameter_grid[parameter] for parameter in parameters]
    iterations = [range(len(parameter_grid[parameter])) for parameter in parameters]

    dirs = []

    for iteration in itertools.product(*iterations):
        iter_stardata = stardata.copy()
        iter_counts = iteration
        run_str = ''
        for i, iter_count in enumerate(iter_counts):
            iter_stardata[parameters[i]] = param_ranges[i][iter_count]
            prefix = '-' if i != 0 else '' 
            run_str += prefix + str(parameters[i]) + '_' + str(iter_count)

        generate_lightcurve(iter_stardata, wavelength, method=method, n_samples=n_samples, shells=shells, n_t=n_t, n_points=n_points, photons=photons, 
                            T_photons=T_photons, gas_2_dust=gas_2_dust, resolution=resolution, root_dir=write_dir + run_str, 
                            cpus=cpus, run_hours=run_hours, memory=memory, job_name=job_name + run_str, 
                            email=email, mcfost_setup=mcfost_setup)
        
        dirs.append(run_str)
        
    # now write a bash script to queue all of the ozstar jobs
    lines = [f'declare -a arr=("{dirs[0]}"\n']
    for directory in dirs[1:]:
        lines.append(f'                "{directory}"\n')
    lines.append('                )\n')
    add_lines = ['for i in "${arr[@]}"\n', 'do\n', f" cd $i\n", f" bash generate_lightcurve.sh\n", f" cd ..\n", "done\n"]
    for line in add_lines:
        lines.append(line)
    bashscript = io.open(f'{write_dir}generate_lightcurve_grid.sh', 'w', newline='\n')
    bashscript.writelines(lines)
    bashscript.close()