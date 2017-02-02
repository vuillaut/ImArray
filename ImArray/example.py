"""
ImArray is a software to image an object in the sky by an array of ground Telescopes
Copyright (C) 2016  Thomas Vuillaume

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

The author may be contacted @
thomas.vuillaume@lapp.in2p3.fr
"""

import geometry as geo
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import object as obj
import CameraImage as ci
import Hillas as hillas
import os
import vizualisation as viz

MEAN = np.empty(0)

# If you want some plots to be done
BoolPlot = False
noise = 0

'''
Shower parameters
'''
impact_point = np.array([0, 10, 0])

# shower direction
salt = math.radians(74)
saz = math.radians(0)

# pointing direction
talt = math.radians(74)
taz = math.radians(0)

# shower parameters
s_top = [0, 0, 15000]
s_bot = [0, 0, 1000]
s_center = [0, 0, 8000]
stop = 15000
slength = 12000
swidth = 200


npoints = 50000


#shower = obj.linear_segment([0,100,15000], s_bot, npoints)
shower = obj.random_ellipsoide(stop, slength, swidth, salt, saz, impact_point, npoints)
#print(shower)


'''
Load a telescope configuration
'''

tel_normal = geo.altaz_to_normal(talt, taz)

tel1 = geo.Telescope([500, 100, -100], tel_normal, 0)
tel2 = geo.Telescope([-10, 300, 100], tel_normal, 0)
tel3 = geo.Telescope([-500, 400, 10], tel_normal, 0)
tel4 = geo.Telescope([-350, -500, 0], tel_normal, 0)
tel5 = geo.Telescope([600, -100, 150], tel_normal, 0)
tel6 = geo.Telescope([300, -300, 50], tel_normal, 0)
tel7 = geo.Telescope([80, 0, 0], tel_normal, 0)
tel8 = geo.Telescope([-80, 0, 0], tel_normal, 0)
tel9 = geo.Telescope([0, -80, 0], tel_normal, 0)
tel10 = geo.Telescope([0, 80, 0], tel_normal, 0)

alltel = [tel7, tel8, tel9, tel10]
# alltel = geo.load_telescopes("data/tel_pos.dat")
# alltel = geo.load_telescopes_flatfloor("data/tel_pos.dat", tel_normal)


# for tel1 in alltel:
#     for tel2 in alltel:
#         if ((tel1.center == tel2.center).all() and tel1.id != tel2.id):
#             print(tel1.id, tel2.id, tel1.center, tel2.center)
print("All telescopes unique : ", geo.telescopes_unicity(alltel))

if BoolPlot:
    viz.plot_shower3d(shower, alltel)

start = time.time()

# file to save images
if not os.path.isdir('results'):
    os.mkdir('results')
f = open('results/teldata.xml', 'w')
f.write("\n")
f.write("<subarray>\n")


triggered_telescopes = []
trigger_intensity = 0.


noise = 0
HP = []

for tel in alltel:
    shower_image = geo.image_shower_pfo(shower, tel)
    shower_cam = geo.site_to_camera_cartesian(shower_image, tel)
    pixels_signal = ci.shower_image_in_camera(tel, shower_cam[:, [0, 1]], noise)

    if len(pixels_signal.nonzero()[0]) > 1 and pixels_signal.sum() > trigger_intensity:
        hp = hillas.hillas_parameters(tel.pixel_tab[:, 0], tel.pixel_tab[:, 1], pixels_signal)
        HP.append(hp)
        triggered_telescopes.append(tel)

pa = hillas.impact_parameter_average(triggered_telescopes, HP, talt, taz)
p = hillas.impact_parameter_ponderated(triggered_telescopes, HP, talt, taz)


print("Real impact parameter : ", impact_point)
print("Reco with simple average = %s \tError = %.2fm" % (pa, math.sqrt(((impact_point - pa) ** 2).sum())))
print("Reco with ponderation and cut = %s \tError = %.2fm" % (p, math.sqrt(((impact_point - p) ** 2).sum())))

# save the results:
#np.savetxt('results/hillas.txt', HP, fmt='%.5f', header="size\t<x>\t<y>\tl\tw\tr\tphi\tpsi\tmiss\tTelId")


# print('\nElapsed (ms):', (time.time() - start) * 1000)

f.write('\n</subarray>')
f.close()

if BoolPlot:
    plt.xkcd()
    plt.legend(loc='upper center', fancybox=True, ncol=3, bbox_to_anchor=(0.5, 1.1))
    plt.show()

plt.close()