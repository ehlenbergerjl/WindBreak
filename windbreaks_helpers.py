import sys
import importlib
import re
import types
import pyperclip
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely import wkt


#%%

def print_functions():
    # List comprehension to get all the functions
    functions = [func for name, func in globals().items()
                 if isinstance(func, types.FunctionType)
                 and not name.startswith('_')
                 and func.__module__ not in ['__builtin__', 'IPython.core.shadowns', 'types']]
    print('\nImported functions are:')
    for func in functions:
        print(func.__name__)


def print_modules():
    # List comprehension to get all the modules
    modules = [mod for name, mod in globals().items()
               if isinstance(mod, types.ModuleType)
               and not name.startswith('_')
               and mod.__name__ not in ['__builtin__', 'IPython.core.shadowns', 'types']]
    print('\nImported modules are:')
    for mod in modules:
        print(mod.__name__)


def print_all_imported_modules():
    print('\nAll imported modules:')
    for name in sys.modules.keys():
        print(name)


def print_cols(df):
    print('\n', 'Dataframe columns:', '\n')
    output_string = ''
    for i, col_name in enumerate(df.columns):
        dtype = df[col_name].dtype
        output_string += f'Index: {i}, Column Name: {col_name}, Data Type: {dtype}\n'
    pyperclip.copy('Dataframe:\n' + output_string)
    print(output_string)


from pyproj import CRS


def get_crs(df):
    crs = CRS(df.crs)
    # Name of the CRS
    print('Name:', crs.name)
    # EPSG of the CRS
    if crs.to_epsg():
        print('EPSG:', crs.to_epsg())
    else:
        print('No EPSG found for this CRS')
    # Unit of the CRS
    print('Unit:', crs.axis_info[0].unit_name)


# %% md
# Define Functions for EDA
# %% md
## - Extent Filter Function that works with the variable 'extents_coords'
# %%
def filter_df_extent(df, extent_coords, lat1, lon1, lat2, lon2):
    min_lat, max_lat = extent_coords['min_lat'], extent_coords['max_lat']
    min_lon, max_lon = extent_coords['min_lon'], extent_coords['max_lon']
    return df[
        ((df[lat1] >= min_lat) & (df[lat1] <= max_lat) &
         (df[lon1] >= min_lon) & (df[lon1] <= max_lon)) |
        ((df[lat2] >= min_lat) & (df[lat2] <= max_lat) &
         (df[lon2] >= min_lon) & (df[lon2] <= max_lon))
        ]


# %% md
## - Convert Geodataframe to a Shapefile
from shapely import wkt


def gdf_to_shp(df, output_file, extent_coords):
    '''
    This function reads a DataFrame, checks for a 'geometry' column or creates one based on latitude and longitude.
    It then filters the DataFrame based on the provided extent coordinates and saves the resultant GeoDataFrame into shapefile format.
    Args:
    df: DataFrame: The input DataFrame.
    output_file: str: Path of the output shapefile.
    extent_coords: dict:
        A dictionary containing the coordinates for area bounds to filter.
        Keys are 'min_lat', 'max_lat', 'min_lon', 'max_lon', belongs to either lat-lon pair.
    Returns:
    None
    '''

    # Check if 'geometry' column exists
    if 'geometry' in df.columns:
        # If 'geometry' column exists, convert it to geometric objects
        df['geometry'] = df['geometry'].apply(lambda x: wkt.loads(x) if pd.notnull(x) else x)
    else:
        # If 'geometry' column does not exist, create it based on 'BEGIN_LAT', 'BEGIN_LON', etc.
        df['geometry'] = [Point(xy) for xy in zip(df['BEGIN_LON'], df['BEGIN_LAT'])]

    # Filter out rows with invalid geometry
    df = df[df['geometry'].notnull()]

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Filter the records that either start or end within the given extents
    gdf_filtered = filter_df_extent(gdf, extent_coords, 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON')

    # Save the GeoDataFrame as a shapefile
    gdf_filtered.to_file(output_file)


# %%
# # Old...
# def gdf_to_shp(gdf, output_file, extent_coords):
#     '''
#     This function reads a GeoDataFrame, and filters it based on latitude and longitude.
#     It then drops NA rows from 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON' and saves the resultant GeoDataFrame into shapefile format.
#     Args:
#     df: GeoDataFrame: The input GeoDataFrame.
#     output_file: str: Path of the output shapefile.
#     extent_coords: dict:
#         A dictionary containing the coordinates for area bounds to the filter.
#         Keys are 'min_lat', 'max_lat', 'min_lon', 'max_lon', belongs to either lat-lon pair.
#     Returns:
#     None
#     '''
#
#     # Filter the records that either start or end within the given extents
#     gdf_filtered = filter_df_extent(gdf, extent_coords, 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON')
#
#     # Save the GeoDataFrame as a shapefile
#     gdf_filtered.to_file(output_file)


# %% md
## - Create Buffer Shapefile from Geodataframe
# %%
def gdf_buf(gdf, distance, output_path):
    '''
    Creates a buffer around the geometries in a given GeoDataFrame and saves the output to a shapefile.

    Args:
    gdf: A GeoDataFrame containing the geometries to buffer
    distance: The distance to buffer around each geometry. This can be a numeric value or a string.
        If a numeric value, the units should be in miles for CRS in State Plane or kilometers for all others.
        If a string, it should end with 'm' for meters or 'ft' for feet.
    output_path: The path to the output shapefile

    Returns:
    A new GeoDataFrame with buffered geometries in the original CRS. Also writes the new GeoDataFrame to a shapefile.
    '''
    original_crs = gdf.crs
    crs_unit = original_crs.axis_info[0].unit_name.lower()

    buffer_distance = distance
    if isinstance(distance, str):
        if distance.endswith('m'):
            buffer_distance = float(distance.rstrip('m'))
            if crs_unit == 'us survey foot' or crs_unit == 'foot':
                buffer_distance *= 3.281
        elif distance.endswith('ft'):
            buffer_distance = float(distance.rstrip('ft'))
            if crs_unit == 'meter':
                buffer_distance /= 3.281
    else:
        if crs_unit == 'degree':
            gdf = gdf.to_crs(epsg=3395)
            crs_unit = gdf.crs.axis_info[0].unit_name.lower()
            buffer_distance = distance * 1000
        elif crs_unit == 'us survey foot':
            buffer_distance = distance * 5280.01016
        elif crs_unit == 'foot':
            buffer_distance = distance * 5280
        elif crs_unit == 'meter':
            buffer_distance = distance * 1000

    gdf['geometry'] = gdf.geometry.buffer(buffer_distance)

    if original_crs != gdf.crs:
        gdf = gdf.to_crs(original_crs)

    gdf.to_file(output_path)

    return gdf
