import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import xenomorph.geometry as gm
import xenomorph as xm
import xenomorph.systems as wrb

def clean_array(arr):
    """
    Converts a NumPy array or masked array to a regular array,
    replacing any non-finite or masked values with 0.
    """
    # If it's a masked array, fill masked values with 0
    if np.ma.isMaskedArray(arr):
        arr = np.ma.filled(arr, fill_value=0.0)
    
    # Convert to regular NumPy array (just in case)
    arr = np.asarray(arr)

    # Replace NaNs and infinities with 0
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)

    return arr

def rotate_correctly(fname):
    from astropy.visualization import simple_norm
    from astropy.wcs import WCS
    from astropy.nddata import CCDData
    from scipy.ndimage import gaussian_filter
    from scipy.ndimage import shift,rotate
    from reproject import reproject_interp,reproject_adaptive
    from reproject.mosaicking import find_optimal_celestial_wcs
    from astropy.visualization import make_lupton_rgb,SqrtStretch,ZScaleInterval
    from matplotlib import cm, colors
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset
    from scipy.signal import find_peaks

    def openFitsImage(file):
        imgfits = fits.open(file)
        img = imgfits[1].data
        hdu = fits.open(file)[1]
        wcs = WCS(hdu.header)
        return img,wcs,imgfits, hdu.header

    img, wcs, hdu, hdr1 = openFitsImage(fname)
    
    wcs_opt, _ = find_optimal_celestial_wcs([hdu[1]])
    img_new = reproject_adaptive(hdu[1], wcs_opt, shape_out = (1300,1300))[0]
    
    return img_new

fname = 'miri_1500W_pid_4093001001_combined_asn_i2d.fits'

jwst_center_x = 752
jwst_center_y = 1000

jwst_data = fits.open(fname)    # for the 2024 epoch

img_new = rotate_correctly(fname)   # rotate to be in the correct WCS

data = clean_array(img_new)  # clean up the NaNs and any infs

pscale = np.sqrt(jwst_data[1].header['PIXAR_A2']) * 1000
im_size = data.shape[0] - jwst_center_y
data = data[(jwst_center_y - im_size):, (jwst_center_x - im_size):(jwst_center_x + im_size)]
length = data.shape[0]

X = np.linspace(-1., 1., length) * pscale * length/2 / 1000
Y = X.copy()

xs, ys = np.meshgrid(X, Y)

data = clean_array(data)

data = data - np.percentile(data, 60)
data = data/np.max(data)
data = np.maximum(data, 0)
data = np.abs(data)**0.3 

for value in data.ravel():
    if np.isnan(value) or np.isinf(value):
        print('gotcha!')


# fig, ax = plt.subplots()

# # ax.pcolormesh(xs, ys, data)
# ax.imshow(data)
# ax.set(aspect='equal')
# plt.show()    

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
        'star1amp':0., 'star1sd':-1., 'star2amp':0., 'star2sd':-1., 'star3amp':0., 'star3sd':-1., 'star3dist':0.}

xm.gui.create_GUI(system=WR125, shells=1, resolution=im_size, reference=[xs, ys, data])
