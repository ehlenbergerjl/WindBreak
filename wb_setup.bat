@echo off
setlocal
:: Add anaconda to local PATH
echo Adding Anaconda to the local PATH...
set "PATH=%UserProfile%\Anaconda3;%UserProfile%\Anaconda3\Library\mingw-w64\bin;%UserProfile%\Anaconda3\Library\usr\bin;%UserProfile%\Anaconda3\Library\bin;%UserProfile%\Anaconda3\Scripts;%PATH%;"

:: Check if the WindBreaks environment already exists
conda info --envs | findstr /C:"WindBreaks" 1>nul
if %errorlevel%==0 (
    echo WindBreaks environment already exists, renaming it to WindBreaks_old...
    conda env create -f windbreaks.yml -n WindBreaks_old || conda env update -f windbreaks.yml -n WindBreaks_old
)

:: Create the conda environment from windbreaks.yml
echo Creating conda environment from windbreaks.yml...
conda env create -f windbreaks.yml -n WindBreaks || (
    echo Failed to create environment. Exiting...
    exit /b 1
)

:: Activate the conda environment
echo Activating the created conda environment WindBreaks...
call activate WindBreaks

:: Run the wb_installs.py script within the environment
echo Running wb_installs.py within the WindBreaks conda environment...
python wb_installs.py || (
    echo "wb_installs.py encountered an error"
    exit /b 1
)

:: Run the wb_jupyter_kernel_install.py script within the environment
echo Running wb_jupyter_kernel_install.py within the WindBreaks conda environment...
python wb_jupyter_kernel_install.py || (
    echo "wb_jupyter_kernel_install.py encountered an error"
    exit /b 1
)

:: Run the wb_notebook_kern_update.py script within the environment
echo Running wb_notebook_kern_update.py within the WindBreaks conda environment...
python wb_notebook_kern_update.py || (
    echo "setup.py encountered an error"
    exit /b 1
)

echo Setup completed successfully.