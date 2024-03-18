:: Check if anaconda is installed and available
where conda >nul 2>nul
IF ERRORLEVEL 1 (
    echo Unable to find Anaconda. Please install it first.

    :: User input choice
    set /P choice="Would you like to download and install Anaconda now? (y/n): "
    if /I "%choice%" EQU "y" (
        echo Attempting to install Anaconda...

        :: Download and Install Latest Anaconda installer using PowerShell
        powershell.exe -Command "
            $anacondaPage = Invoke-WebRequest -Uri 'https://www.anaconda.com/products/distribution/'
            $installerUrl = ($anacondaPage.ParsedHtml.getElementsByTagName('a') | Where-Object {$_.href -like '*Anaconda3-*-Windows-x86_64.exe'}).href
            $installerName = [System.IO.Path]::GetFileName($installerUrl)

            # Download Anaconda installer
            Write-Host 'Downloading' $installerName '...'
            Invoke-WebRequest -Uri $installerUrl -OutFile $installerName

            # Install Anaconda
            Write-Host 'Installing' $installerName '...'
            Start-Process -Wait -FilePath $installerName -ArgumentList '/InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Anaconda3'
        "

        :: Check if installation successful
        where conda >nul 2>nul
        IF ERRORLEVEL 1 (
            echo Error in Anaconda configuration. Exiting...
            exit /b 1
        )

        :: Add anaconda to PATH
        setx PATH "%UserProfile%\Anaconda3;%UserProfile%\Anaconda3\Library\mingw-w64\bin;%UserProfile%\Anaconda3\Library\usr\bin;%UserProfile%\Anaconda3\Library\bin;%UserProfile%\Anaconda3\Scripts;%PATH%"
    ) ELSE (
        echo Skipping Anaconda installation. Exiting...
        exit /b 1
    )
)

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