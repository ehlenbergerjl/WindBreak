# Create new env
conda create --name WindBreaks
# Activate new env
conda activate WindBreaks
# Install the packages
python -m pip install jupyter
conda install -c anaconda ipykernel --yes
conda install -c conda-forge IPython --yes
conda install -c conda-forge netCDF4 --yes
conda install -c conda-forge rasterio --yes
conda install -c conda-forge numpy --yes
conda install -c conda-forge xarray --yes
conda install -c pyviz hvplot --yes
conda install -c conda-forge holoviews --yes
conda install -c anaconda pandas --yes
conda install -c anaconda seaborn --yes
conda install -c conda-forge matplotlib --yes
conda install -c anaconda regex --yes
conda install -c conda-forge cartopy --yes
conda install -c conda-forge ipywidgets --yes

# Create the Jupyter Kernal for your notebook
python -m ipykernel install --user --name WindBreaks --display-name "WindBreaks"

