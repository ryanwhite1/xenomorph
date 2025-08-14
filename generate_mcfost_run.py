import xenomorph as xm 
import xenomorph.mcfost as xmc
import xenomorph.systems as wrb
import os

# root_dir = 'rad_transfer/apep/1shell_lowres'
# n_t, n_points = 120, 30
# root_dir = 'rad_transfer/apep/1shell_lowishres'
# n_t, n_points = 200, 50
# root_dir = 'rad_transfer/apep/1shell_medres'
# n_t, n_points = 300, 100
# root_dir = 'rad_transfer/apep/1shell_highres'
root_dir = 'rad_transfer/apep/1shell_highres3'
n_t, n_points = 600, 200

photons = 2e7
if not os.path.exists(root_dir):
    os.makedirs(root_dir)


system = wrb.apep.copy()
system['phase'] = 0.15

density_file = 'apep1shell.fits'
para_file = 'apep'
wavelength = 3.4    # microns
resolution = 30

xmc.mcfost_points(system, 1, 1e-5, density_file, n_t=n_t, n_points=n_points, resolution=resolution, root_dir=root_dir)
xmc.generate_para(para_file, density_file, distance=2400, photons=photons, T_photons=1e7, resolution=resolution, gas_2_dust=100, root_dir=root_dir)
xmc.generate_slurm(para_file, 3.4, para_file+'.para', density_file, cpus=8, run_hours=20, root_dir=root_dir)