
#!/bin/bash

# Check if conda is installed and available
if ! command -v conda &> /dev/null
then
    echo "Unable to find Conda. Please install it first."
    exit
fi

# Create the conda environment from environment.yml
echo "Creating conda environment from environment.yml..."
conda env create -f environment.yml

# Activate the conda environment
echo "Activating the created conda environment WindBreaks..."
source activate WindBreaks

# Run the installs.py script within the environment
echo "Running installs.py within the WindBreaks conda environment..."
python wb_installs.py

echo "Setup completed successfully."