# updated 16 SEP 2022 from bajaAW version - testing on CIRES laptop
# goal is to include the various area of interest grid regions in a single file to avoid divergence of multiple versions
# rick saltus
#

import os
import numpy as np
import sys
from pyproj import Proj, transform
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import statistics
import time
from scipy.stats import binned_statistic_2d
import warnings 

# set variables
outfname = "DataFiles/BajaAngelWingsStatsOUT.csv"
inFile = "DataFiles/BajaAngelWingsXYZuIN.csv"

# if input coordinates are lat/long, set latlon to TRUE and then provide input and desired ouput projection information
latlon = True
inProj = "epsg:4326"
# Baja Angel Wings projection (UTM 11)
outProj = "epsg:32611"
# End of projection definitions
outFile = open(outfname,"w")
outFile.write("northing,easting,average,weighted_average,median,standard_deviation,uncertainty,weighted_average2,standard_deviation_WM2, standard_deviation_NIST,num_points"+"\n")


# grid specifics, based on metadata of target grid
cellsize = 4000
#Baja Angel Wings Grid bounds
x_top_right = 436000
y_top_right = 3992000
x_bottom_left = -16000
y_bottom_left = 3536000
#

# ignore warnings
warnings.filterwarnings("ignore")


def project_array(coordinates, srcp=inProj, dstp=outProj):
    """
    Project a numpy (n,2) array in projection srcp to projection dstp
    Returns a numpy (n,2) array.
    """
    p1 = Proj(init=srcp)
    p2 = Proj(init=dstp)
    fx, fy = transform(p1, p2, coordinates[:,0], coordinates[:,1])
    # Re-create (n,2) coordinates
    return fx, fy

def meshgrid2(*arrs):
    arrs = tuple(reversed(arrs))
    lens=list(map(len, arrs))
    dim = len(arrs)
    sz = 1
    for s in lens:
        sz *= s
        ans = []
    for i, arr in enumerate(arrs):
        slc = [1]*dim
        slc[i] = lens[i]
        arr2 = np.asarray(arr).reshape(slc)
        for j, sz in enumerate(lens):
            if j != i:
                arr2 = arr2.repeat(sz, axis=j)
        ans.append(arr2)
    return tuple(ans)

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

t1 = time.time()

df = pd.read_csv(inFile)

X = df["X"].values
Y = df["Y"].values
Z = df["Z"].values
U = df["uncertainty"].values

if latlon == True:
    coordinates = np.vstack((X, Y)).T
    X, Y = project_array(coordinates)

x = np.arange(x_bottom_left,x_top_right+cellsize,cellsize)
y = np.arange(y_bottom_left, y_top_right+cellsize,cellsize)

g = meshgrid2(y,x)

pos = np.vstack(map(np.ravel, g)).T

x = np.arange(x_bottom_left-cellsize/2, x_top_right + cellsize + cellsize/2, cellsize)
y = np.arange(y_bottom_left-cellsize/2, y_top_right + cellsize+ cellsize/2, cellsize)

count = binned_statistic_2d(X,Y,Z,'count',bins=[x,y])
count = count.statistic.ravel()

counter = 0

for position in pos:

	if count[counter] > 1:

		data = []
		wdata = 0
		wdata2 = 0
		uncertainty = []
		iuncertainty = 0
		iuncertaintysq = 0

		ymin = position[1] - cellsize/2
		ymax = position[1] + cellsize/2
		xmin = position[0] - cellsize/2
		xmax = position[0] + cellsize/2

		indices_x = list(map(list,np.where(np.logical_and(X>=xmin, X<xmax))))[0]
		indices_y = list(map(list,np.where(np.logical_and(Y>=ymin, Y<ymax))))[0]
		indices = intersection(indices_x, indices_y)

		for _i in indices:
			data.append(Z[_i])
			uncertainty.append(U[_i])
			wdata = wdata + Z[_i]/U[_i]
			iuncertainty = iuncertainty + 1/U[_i]
			iuncertaintysq = iuncertaintysq + 1/(U[_i]*U[_i]) # this is column D in the spreadsheet
			wdata2 = wdata2 + Z[_i]/U[_i]**2 # this is column E in the spreadsheet

		if len(data) > 1:
			avg = np.mean(data)
			std = np.std(data,ddof=1)
			num_points = len(data)
			median = np.median(data)
			weighted_mean = wdata / iuncertainty
			uncert = np.sqrt(1/iuncertaintysq)
			weighted_mean2 = wdata2 / iuncertaintysq

			data_minus_WM2 = []
			f_squared = []
			wgt_f_squared = []

			for _i in range(len(data)):
				data_minus_WM2.append(data[_i] - weighted_mean2)
				f_squared.append(data_minus_WM2[_i]**2)
				wgt_f_squared.append(f_squared[_i]*(1/uncertainty[_i]**2))
                
                

			standard_deviation2 = np.sqrt(np.sum(f_squared)/(len(data)-1))
			standard_deviation_NIST = np.sqrt(np.sum(wgt_f_squared)/(((len(data)-1)*np.sum(iuncertaintysq))/(len(data))))


			outFile.write(str(position[1])+","+str(position[0])+","+str(avg)+","+str(weighted_mean)+","+str(median)+","+str(std)+","+str(uncert)+","+str(weighted_mean2)+","+str(standard_deviation2)+","+str(standard_deviation_NIST)+","+str(num_points)+"\n")

		counter = counter + 1

	else:
		counter = counter + 1


outFile.close()

print("Time elapsed: "+ str(round(time.time()-t1,3))+" seconds")
