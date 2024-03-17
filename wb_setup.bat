:: Check if conda is installed and available
where conda >nul 2>nul
IF ERRORLEVEL 1 (
    echo Unable to find Conda. Please install it first.
    exit
)

:: Create the conda environment from environment.yml
echo Creating conda environment from windbreaks.yml...
conda env create -f windbreaks.yml

:: Activate the conda environment
echo Activating the created conda environment WindBreaks...
call activate WindBreaks

:: Run the installs.py script within the environment
echo Running installs.py within the WindBreaks conda environment...
python wb_installs.py

echo Setup completed successfully.