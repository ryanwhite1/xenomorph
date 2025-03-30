import numpy as np

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

