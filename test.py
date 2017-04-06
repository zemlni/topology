from liblas import file
from TDA import *
import numpy as np
import matplotlib.pyplot as plt


f = file.File('/home/nikita/Projects/topology/NEON_AOP_sample_data_v2/LiDAR/Discrete_LiDAR/Point_Cloud/2013_SJER_AOP_point_cloud_classified.las',mode='r')

array = []
i = 0
for point in f:
    #print 'X,Y,Z: ', point.x, point.y, point.z
    if i % 1000 == 0:
        array.append([float(point.x), float(point.y), float(point.z)])
    i += 1
f.close()
del(f)
print(len(array))
array = np.asarray(array)

PDs = doRipsFiltration(array, 1)
PD = PDs[1]

plotDGM(PD)
plt.show()
