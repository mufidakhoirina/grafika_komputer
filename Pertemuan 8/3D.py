# Membuat Gambar 3D dari data X,Y,Z
# Asep Hermawan, Mei 2020

import matplotlib.pyplot as plt
import scipy.interpolate
import numpy as np

# Data
X = [1, 2, 3, 4, 1, 1, 2, 3, 0, 3, 4, 2]
Y = [1, 1, 0, 1, 2, 3, 2, 2, 3, 3, 4, 4]
Z = [100, 220, 250, 350, 220, 200, 300, 550, 200, 350, 400, 250]

#Membuat grid x dan y
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 50)
xi, yi = np.meshgrid(x, y)

#interpolasi harga X, Y, Z
rbf = scipy.interpolate.Rbf(X, Y, Z) 
z = rbf(xi, yi)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, z, cmap='seismic', edgecolor='none' )
ax.contour(x, y, z, 10, colors= 'black')

plt.show()