import rasterio
import numpy as np
import os
import glob
from scipy.spatial import cKDTree

# PART 1

# define control variables
file_dir = "C:\\Users\\catan\\Desktop\\GEOG5092\\lab4\\data\\data"
raster_files = glob.glob(file_dir + '\*.tif')
winrows = 11
wincols = 9

# raster prep
slope_ras = rasterio.open(os.path.join(file_dir, 'slope.tif'))
wind_ras = rasterio.open(os.path.join(file_dir, 'ws80m.tif'))
urban_ras = rasterio.open(os.path.join(file_dir, 'urban_areas.tif'))
water_ras = rasterio.open(os.path.join(file_dir, 'water_bodies.tif'))
protected_ras = rasterio.open(os.path.join(file_dir, 'protected_areas.tif'))

slope_arr = slope_ras.read(1)
wind_arr = wind_ras.read(1)
urban_arr = urban_ras.read(1)
water_arr = water_ras.read(1)
protected_arr = protected_ras.read(1)

#accounting for zeros
wind_arr = np.where(wind_arr < 0, 0, wind_arr)
slope_arr = np.where(slope_arr < 0, 0, slope_arr)

metadata = wind_ras.meta

# moving window function

def mean_array(temp_arr, window):
    pct_arr = np.zeros(temp_arr.shape)
    window_area = float(window.sum())
    
    rowdim = window.shape[0]//2
    coldim = window.shape[1]//2
    
    for row in range(rowdim,temp_arr.shape[0] - rowdim):
        for col in range(coldim,temp_arr.shape[1] - coldim):
            window = temp_arr[row - rowdim: row + rowdim + 1,
                              col - coldim: col + coldim + 1]
            pct_arr[row,col] = window.sum()
    return pct_arr / window_area

# step 2

# slope
slope_sites = mean_array(slope_arr, window)
slope_sites = np.where(slope_sites > 15, 0, 1)
# wind
wind_sites = mean_array(wind_arr, window)
wind_sites = np.where(wind_sites > 8.5, 1, 0)
# urban sites
urban_sites = mean_array(urban_arr, window)
urban_sites = np.where(urban_sites != 1, 1, 0)
# water bodies
water_sites = mean_array(water_arr, window)
water_sites = np.where(water_sites < 0.02, 1, 0)
# protected areas
protected_sites = mean_array(protected_arr, window)
protected_sites = np.where(protected_sites < 0.05, 1, 0)

# step 3

sum_array = slope_sites + wind_sites + urban_sites + water_sites + protected_sites
suitability_test = np.where(sum_array == 5, 1, 0)

# step 4: Convert your final numpy suitability array to a geotif raster file for visualization purposes.

with rasterio.open(r"C:\Users\catan\Desktop\GEOG5092\lab4\data\data\slope.tif") as dataset:
   with rasterio.open(f'suitable_sites.tif', 'w',
                 driver = 'GTiff',
                 height= sum_array.shape[0],
                 width=sum_array.shape[1],
                 count=1,
                 dtype=np.int32,
                 crs=dataset.crs,
                 transform=dataset.transform,
                 ndata =dataset.nodata
                 ) as tif_dataset:
        tif_dataset.write(sum_array,1)
        
# step 5

print('There are', suitability_test.sum(), 'suitable sites.')

# PART 2

with rasterio.open(r"C:\Users\catan\GEOG5092\lab4\suitable_sites.tif") as file:
    bounds = file.bounds
    upper_bound = (bounds[0], bounds[3])
    lower_bound = (bounds[2], bounds[1])
    cell_size = 1000
    
    x_coords = np.arange(upper_bound[0] + cell_size / 2, lower_bound[0], cell_size)
    y_coords = np.arange(lower_bound[1] + cell_size / 2, upper_bound[1], cell_size)
    
    x,y = np.meshgrid(x_coords, y_coords)
    cent_coords = np.c_[x.flatten(), y.flatten()]
    
suitable_cent_coords = []
for sx, sy in zip(cent_coords, suitability_test.flatten()):
    xx = np.multiply(sx[0], sy)
    yy = np.multiply(sx[1], sy)
    if xx != 0 and yy != 0:
        suitable_cent_coords.append([xx,yy])

dist, i = cKDTree(stations).query(suitable_cent_coords)
print("The shortest distance is ", np.min(dist)/1000, "kilometers and the longest distance is ", np.max(dist)/1000, "kilometers.")