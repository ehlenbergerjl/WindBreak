# Getting started

Intstall the latest [MiniConda](https://docs.anaconda.com/free/miniconda/) for your Operating System

- When asked, I recommend you install for 'Just me', not 'All users'
- This is important if you are not admin on your system

Create your environment in a Python shell (Terminal in PyCharm)

- Replace 'myenv' with whatever name you want to give your new environment
- I'm calling mine 'WindBreaks'
  Install these packages with the '--yes' option to keep it moving without asking questions
- ... or you can leave that out if you want to know what is being upgraded/downgraded/installed for compatibility and
  dependency

Here is an example:

    # Create new env
    conda create --name myenv
    # Activate new env 
    conda activate myenv
    # Install the packages
    python -m pip install jupyter
    conda install conda-content-trust --yes
    conda install -c anaconda ipykernel --yes
    conda install -c conda-forge IPython --yes
    conda install -c conda-forge netCDF4 --yes
    conda install -c conda-forge rasterio --yes
    conda install -c conda-forge numpy --yes
    conda install -c conda-forge xarray --yes
    conda install -c pyviz hvplot --yes
    conda install -c conda-forge holoviews --yes
    conda install -c anaconda pandas --yes
    conda install -c conda-forge geopandas --yes
    conda install -c conda-forge rasterstats --yes
    conda install -c anaconda seaborn --yes
    conda install -c conda-forge matplotlib --yes
    conda install -c anaconda regex --yes
    conda install -c conda-forge cartopy --yes
    conda install -c conda-forge ipywidgets --yes

    # Create the Jupyter Kernal for your notebook
    python -m ipykernel install --user --name WindBreaks --display-name "WindBreaks"

## Possible additional resources:

### Tutorials

#### Exploratory Analysis

- [Tutorial 1](https://www.geeksforgeeks.org/quick-guide-to-exploratory-data-analysis-using-jupyter-notebook/)
- [YOUR Data Teacher (YouTube video)](https://www.youtube.com/watch?v=iZ2MwVWKwr4)

# Project Notes:

## Standardization:

### Colors

- April red hex E41A1C
- May blue hex 377EB8
- June green hex 4DAF4A

# Data Sources:

- [NOAA Local Climate Data (LCD)](https://www.ncei.noaa.gov/maps/lcd/)
- [NOAA Storm Events (NCEI)](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/)
- [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/cdsapp#!/home)
- [Climatology Lab](https://www.climatologylab.org/gridmet.html)

# EXPLORATORY DATA ANALYSIS

1) Describe the Data
2) Trends
3) Summary tables
4) drop unneeded columns
5) drop duplicates
6) drop outliers

## Update from Bhuwan & possible tasks for next week and beyond: (3/27/2024)

###  * Task 1 - see if you can create a summary statistics using this data and find any relationship between the storm events and crop damages

- I have added storm event line shape file. It has details about the storm intensity, etc.
- The file is called “stormevents_line_details.shp” and its
  in [this folder](https://drive.google.com/drive/u/1/folders/1EWWnjXzVrVY3GUTp3hwoWEh5UsmP2E_E).
- Maybe we can create a smaller size buffer. I used 5 mile buffer of the line and I think it was too big.
- You will have to aggregate the storm events data at county-level to compare it with crop loss because crop loss is at
  the county level only.

## Update from Bhuwan & possible tasks for next week and beyond: (3/30/2024)

###  * Task 2 - Mean monthly wind speed (netcdf data)

- Considering the time constraints, let’s use the mean monthly wind speed data
  from [this folder](https://drive.google.com/drive/folders/1zxvOB6XwXkiOWh1QhQyzTEd5VrL87Puw?usp=drive_link).
- The data source is [climatologylab.org](https://www.climatologylab.org/gridmet.html)
- Pick any one year and do the analysis, (1) spatial and temporal trends of wind speed in the study area, (2) its
  relationship with crop loss (correlation coefficient).  
