import matplotlib.pyplot as plt
import jax.numpy as jnp

import xenomorph.systems as wrb
import xenomorph.geometry as gm

# set LaTeX font for our figures
plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'

pixel_scale = 0.007280453888888889
n_pixels = 99

bound = (n_pixels * pixel_scale / 2) * (1. + 2. / n_pixels)

bins = jnp.linspace(-bound, bound, n_pixels+1)


system = wrb.WR137.copy()
system['arg_peri'] = 180.6
system['open_angle'] = 37.2

particles, weights = gm.dust_plume(system)

print(weights)
print(particles)
X, Y, H = gm.smooth_histogram2d_w_bins(particles, weights, system, bins, bins)
# H = gm.add_stars(X[0, :], Y[:, 0], H, system)

print(X.shape, H.shape)
print(H)

fig, ax = plt.subplots(figsize=(6, 6))
ax.pcolormesh(X, Y, H, cmap='hot', rasterized=True)
ax.set(aspect='equal', xlabel='Relative RA (")', ylabel='Relative Dec (")')

fig.savefig('test.png')