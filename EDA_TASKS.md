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
