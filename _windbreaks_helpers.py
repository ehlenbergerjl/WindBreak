import sys
import os
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


# def print_cols(df):
#     print('\n', 'Dataframe columns:', '\n')
#     output_string = ''
#     for i, col_name in enumerate(df.columns):
#         dtype = df[col_name].dtype
#         output_string += f'Index: {i}, Column Name: {col_name}, Data Type: {dtype}\n'
#     pyperclip.copy('Dataframe:\n' + output_string)
#     print(output_string)


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


def gdf_to_shp(gdf, output_file, extent_coords):
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

    # Filter the records that either start or end within the given extents
    gdf_filtered = filter_df_extent(gdf, extent_coords, 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON')

    # Save the GeoDataFrame as a shapefile
    gdf_filtered.to_file(output_file)


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


def combine_files(src_dir, years=None, states=None):
    # Load the header file
    header_tbl = pd.read_csv(os.path.join(src_dir, 'crop_loss_COL/colsom_headers.csv'), header=None,
                             encoding='iso-8859-1')

    # Get the headers from the 2nd column (index 1) of the header DataFrame
    tbl_headers = header_tbl.iloc[:, 1].values.tolist()  # convert to list for use as headers

    dataframes = []  # list to hold dataframes

    # If no years provided, default to 2000-present
    if not years:
        from datetime import datetime
        start_year = 2000
        current_year = datetime.now().year
        years = [str(int(year)) for year in
                 range(start_year, current_year + 1)]  # this will create a list of years from 2000 to the present

    for year in years:
        filename = f'crop_loss_COL/colsom_{year}.txt'
        try:
            df = pd.read_csv(os.path.join(src_dir, filename), sep='|', header=None)
            df.columns = tbl_headers  # Set the headers immediately after loading

            # Filter based on the 'Year of Loss' column
            df = df.dropna(subset=['Year of Loss'])  # remove NaN values
            df['Year of Loss'] = df['Year of Loss'].apply(
                lambda x: str(int(x)))  # converting year of loss from float to string
            df = df[df['Year of Loss'].isin(years)]

            # If list of states is provided, filter the dataframe based on those states
            if states:
                df = df[df['State Abbreviation'].isin(
                    states)]  # Now the column name can be used because the headers are already set

            dataframes.append(df)
        except FileNotFoundError:
            print(f'File {filename} not found.')

    # concatenate all dataframes
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # assign headers to concatenated dataframe
    concatenated_df.columns = tbl_headers

    return concatenated_df


def remove_outliers(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    df_out = df[~((df[column_name] < (Q1 - 1.5 * IQR)) | (df[column_name] > (Q3 + 1.5 * IQR)))]
    return df_out

# %%
