import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc

# reading in netcdf
netcdf = nc.Dataset('/Users/gghope/Documents/S24 School Stuff/GIScience Seminar/vs_2017.nc', mode='r')
# separating wind speed into numpy array
wind_speed = np.array(netcdf.variables['wind_speed'])
# separating lats and longs into numpy arrays
longs = np.array(netcdf.variables['lon'])
lats = np.array(netcdf.variables['lat'])
# closing netcdf file
netcdf.close()

# establish empty arrays for coordinates
xs = []
ys = []
zs = []

# iterate through lats and longs to get z value (wind speed) for each lat/lon pair
# iterate through each latitude in the dataset
for lat in range(len(lats)):
    # iterate through each longitude for the given latitude
    for lon in range(len(longs)):
        # create list of wind speeds for given lat/long pair
        total = list(filter(lambda x: x<=1000, wind_speed[::, lat, lon]))
        if len(total) > 0:
            # average all wind speeds for given lat/long pair
            maximum = max(total)
            # add data to empty arrays
            xs.append(longs[lon])
            ys.append(lats[lat])
            zs.append(maximum)

plt.hist(zs)
plt.show()