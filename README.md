# WindBreaks Group2

## Group 2: Wind speed and wind event data: 
#### Group members names (Two members): Jason Ehlenberger, Gloria Hope
## Overall objective:  
This group will work on the wind speed data.  Your goal of this analysis is to explore the data and explain the key messages from the data (a) what kind of insights can we get from the data, (b) why do we see particular trend in the data, and (c) is there any relationship between these wind and crop loss variables (COL data). 
### About the dataset: 
- HRRR data: This is a bit complex data. It provides hourly wind speed for the whole USA. Or may be we can use some data from COPERNICUS or other sources. [TO BE UPLAODED]
- Storm event data: This is a point/line data that provides information on wind-related events like tornadoes, etc for the whole USA. 
- Crop Loss Data (COL): This is the monthly data of crop loss by cause of loss at a county level. We will study 2014 to 2021 and for four counties. However, you are open to study at a national level and for a longer time scale as the data is available from 1990 to 2024.  
-- https://www.rma.usda.gov/SummaryOfBusiness/CauseOfLoss 
- Crop cover data (30 m): This raster data provides yearly crop cover for the whole USA. That means in what crop we grow across the country. This team will try to use this information as well to make some conclusive findings (zonal statistics). [MINIMAL USE OF THIS DATA]
-- https://nassgeodata.gmu.edu/CropScape/ 
### Suggested data carpentry and analysis (feel free to add your own analysis):
1) Exploratory analysis of wind speed data and wind event data: 
   - This is the most complex data (cubical data) on monthly wind speed.
   - Where do we see high wind events in the study area? 
3) Time series maps of the high wind event.
   - Spatial map of which places receive the most wind events and when?
4) Histogram to understand the distribution of the data. 
5) Spatial and temporal analysis of the wind speed and wind event data and its relationship with crop loss (COL data):
   - Since we know that crop loss is directly proportional to wind speed, we will try to explore the relationship here. What types of wind variables have high correlation with crop loss? Is it maximum wind speed, number of high wind speed events in a given month, or something else?
   - By overlaying the wind speed over the crop cover data (raster data), we can see which crops these high wind events generally damage and when?
   - Since crop loss data is available at a monthly time scale at county level, we need to aggregate the wind data at the county level.
   - What kind of aggregation would you need to do to explore its relationship with crop loss? E.g. (just thoughts) the number of medium vs high wind events in a month for a particular county, the number of tornadoes in the county, etc. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Make sure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your machine.

### Installing

To get a local copy of the code, clone it using git:
bash git clone https://github.com/ehlenbergerjl/WindBreak.git

Or, you can do this directly in PyCharm or DataSpell:

1. In the Welcome screen, click on "Get from VCS".
2. In the Version Control window, paste the following URL: https://github.com/ehlenbergerjl/WindBreak.git
3. Choose the directory where you want the project to be on your local machine and click "Clone".

After the project has been cloned, PyCharm or DataSpell will prompt to open the project. Click "Yes" and the IDE will load the project for you.

Navigate to the project directory if neccesary:
cd <project-directory>

Run the setup script in PowerShell:
wb_setup.bat

This will create and activate the Conda environment `WindBreaks` and install all the necessary packages.
### Running the project

Now you can run the project using:
python python group2_main.py

## Authors

- Jason Ehlenberger
- Gloria Hope

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License - see the [LICENSE.md](LICENSE.md) file for details
