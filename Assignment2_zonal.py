import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import rasterio
import rasterstats
from rasterio.warp import calculate_default_transform, reproject, Resampling

# %%
# Set file paths and CRS
dst_crs = 'EPSG:6469'
src_fp = 'crop_cover_2019.tif'
dst_fp = 'crop_cover_2019_prj_9712.tif'
fn = 'counties_subset_Albers4.shp'
ext_dir = r'C:\Users\ehlenbergerjl\DataspellProjects\WindBreaks\Data\Assignment2'

# %%
# Reproject raster
with rasterio.open(src_fp) as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height,
        'nodata': 255
    })
    with rasterio.open(dst_fp, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)

# %%
# Read and plot reprojected raster
raster = rasterio.open(dst_fp)
show(raster, 1, cmap='Blues')
show_hist(raster, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histogram")

# %%
# Read shapefile and reproject
gdf = gpd.read_file(fn)
gdf = gdf.to_crs(dst_crs)

# %%
# Perform zonal statistics
crop_lst = [1, 5, 6, 23, 24, 26, 225, 226, 236, 237, 238, 240, 241, 254]
crop_dict = {1: 'Corn', 5: 'Soybeans', 6: 'Sunflower', 23: 'Spring Wheat', 24: 'Winter Wheat',
             26: 'Dbl Crop WinWht/Soybeans', 225: 'Dbl Crop WinWht/Corn', 226: 'Dbl Crop Oats/Corn',
             236: 'Dbl Cropp WinWht/Sorghum', 237: 'Dbl Crop Barley/Corn', 238: 'Dbl Crop WinWht/Cotten',
             240: 'Dbl Crop Soybeans/Oats', 241: 'bl Crop Corn/Soybeans', 254: 'Dbl Crop'}
raster_data = raster.read(1)
crop_mask = np.isin(raster_data, crop_lst)
masked_raster_data = np.where(crop_mask, raster_data, -1)
stats = zonal_stats(gdf, masked_raster_data, affine=raster.transform, categorical=True)
named_stats = [{crop_dict.get(k, k): v for k, v in zone.items()} for zone in stats]

# %%
# Convert stats to DataFrame and calculate additional metrics
crop_stats_df = pd.DataFrame(named_stats)
crop_stats_df['Zone'] = crop_stats_df.index + 1
crop_stats_df['Total_Count'] = crop_stats_df.sum(axis=1)
crop_stats_df['Dominant_Crop'] = crop_stats_df.drop(columns=['Zone', 'Total_Count']).idxmax(axis=1)
proportions_df = crop_stats_df.drop(columns=['Zone', 'Total_Count', 'Dominant_Crop']).div(crop_stats_df['Total_Count'],
                                                                                          axis=0)

# %%
# Plot proportions
proportions_df.plot(kind='bar', stacked=True, legend=True)
plt.title('Crop Proportions by Zone')
plt.xlabel('Zone')
plt.ylabel('Proportion of Total Count')
plt.show()

# %%
# Merge FIPS codes and county names with stats
geoid = pd.DataFrame(gdf[['GEOID', 'NAME']])
geoid.columns = ['FIPS', 'County_Name']
merged_df = pd.merge(pd.DataFrame(named_stats), geoid, left_index=True, right_on='County_Name')
print(merged_df)
# %%
