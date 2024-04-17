import os
import sys
import types
from datetime import datetime

import geopandas as gpd
import matplotlib.colors as colors
import pandas as pd
import pyperclip
from matplotlib.colors import Normalize
from matplotlib.path import Path
from shapely.geometry import LineString


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
    pyperclip.copy('Dataframe columns:\n' + output_string)
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

def df_gdf_or_csv_to_shp(source, output, extent_coords):
    """
    This function reads a CSV file and filters it based on latitude and longitude.
    Then it drops NA rows from 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON' and converts the DataFrame into GeoDataFrame.
    Finally, the output is saved into shapefile format.

    Args:
    source_file: str: Path of the source CSV file.
    output_file: str: Path of the output shapefile.
    extent_coords: dict:
        A dictionary containing the coordinates for area bounds to the filter.
        Keys are 'min_lat', 'max_lat', 'min_lon', 'max_lon', belongs to either lon-lat pair.

    Returns:
    None
    """

    if isinstance(source, str):
        # if source is a string (filepath), then load it as DataFrame
        df = pd.read_csv(source)
    elif isinstance(source, pd.DataFrame) or isinstance(source, gpd.GeoDataFrame):
        # if source is DataFrame or GeoDataFrame, then use it as is
        df = source
    else:
        raise ValueError('Invalid type for source. Source should be a file path (str) or DataFrame/GeoDataFrame')

    # Pull out bounds for easier reference
    min_lat, max_lat = extent_coords['min_lat'], extent_coords['max_lat']
    min_lon, max_lon = extent_coords['min_lon'], extent_coords['max_lon']

    # Filter the records that either start or end within the given extents
    df_filtered = df[
        (
                (df['BEGIN_LAT'] >= min_lat) &
                (df['BEGIN_LAT'] <= max_lat) &
                (df['BEGIN_LON'] >= min_lon) &
                (df['BEGIN_LON'] <= max_lon)
        ) |
        (
                (df['END_LAT'] >= min_lat) &
                (df['END_LAT'] <= max_lat) &
                (df['END_LON'] >= min_lon) &
                (df['END_LON'] <= max_lon)
        )
        ]

    # Drop NA values from 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON'
    df_filtered = df_filtered.dropna(subset=['BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON'])

    # Create a new 'geometry' column in the DataFrame that contains LineString objects
    df_filtered['geometry'] = df_filtered.apply(lambda row: LineString(
        [(row['BEGIN_LON'], row['BEGIN_LAT']), (row['END_LON'], row['END_LAT'])]), axis=1)

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df_filtered, geometry='geometry')

    # Set the GeoDataFrame's coordinate reference system to NAD83
    gdf.set_crs(epsg=4269, inplace=True)

    # Save the GeoDataFrame as a shapefile
    gdf.to_file(output)

    return gdf

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


def combine_csv_files(src_dir, prefix):
    # List of all the csv files beginning with specified prefix
    csv_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.startswith(prefix) and f.endswith('.csv')]

    # Combine all into one GeoDataFrame
    combined_gdf = pd.concat((gpd.read_file(f) for f in csv_files))

    return combined_gdf


def month_name_to_number(month_name):
    datetime_object = datetime.strptime(month_name, "%B")
    # We use +1 because January maps to 0 and December maps to 11
    return datetime_object.month
# %%
# Define a function to convert to millions
def millions(x, pos):
    return '%1.1fM' % (x * 1e-6)
