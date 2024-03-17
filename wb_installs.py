
import os
import subprocess
from importlib.metadata import version, PackageNotFoundError


def install_package_with_conda(package):
    '''Install a package using conda.

    Args:
        package (str): The name of the package to install.

    Returns:
        bool: True if installation succeeded, False otherwise.
    '''
    try:
        subprocess.check_call(['conda', 'install', '-y', package])
        return True
    except subprocess.CalledProcessError:
        print(f'Failed to install "{package}" using conda.')
        return False


def install_package_with_pip(package):
    '''
    Installs a package using pip.

    Parameters:
    - package (str): The name of the package to install.

    Returns:
    - bool: True if the package was installed successfully, False otherwise.

    Example Usage:
    install_package_with_pip('requests')
    '''
    try:
        subprocess.check_call(['python', '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        print(f'Failed to install "{package}" using pip.')
        return False


def get_package_version(package):
    '''
    Get the version of a given package.

    Args:
        package (str): The name of the package.

    Returns:
        str or None: The version of the package if found, otherwise None.

    Raises:
        PackageNotFoundError: If the package is not found.
    '''
    try:
        return version(package)
    except PackageNotFoundError:
        return None


def check_and_install_package(package, use_pip=False):
    '''
    Checks if a package is installed and installs it if not.

    Parameters:
    - package (str): The name of the package to check and install.
    - use_pip (bool): Optional. Specifies whether to use pip for installation. Default is False.

    Returns:
    A tuple (success, version):
    - success (bool): True if the package is installed successfully, False otherwise.
    - version (str or None): The installed version of the package. None if installation failed.

    Example usage:
    success, version = check_and_install_package('numpy')
    if success:
        print(f''numpy' version {version} is installed.')
    else:
        print('Failed to install 'numpy'.')
    '''
    installed_version = get_package_version(package)
    if installed_version:
        print(f'"{package}" is already installed with version: {installed_version}')
        return True, installed_version
    else:
        print(f'"{package}" is not installed. Installing...')
        if use_pip:
            success = install_package_with_pip(package)
        else:
            success = install_package_with_conda(package)
            if not success:
                success = install_package_with_pip(package)

        if success:
            installed_version = get_package_version(package)
            print(f'Successfully installed "{package}" with version: {installed_version}')
        else:
            print(f'Failed to install "{package}".')
            installed_version = None

        return success, installed_version


packages = ['matplotlib', 'numpy', 'pandas', 'pygal', 'ipyleaflet']
pip_only_packages = ['geopandas', 'rasterstats', 'geoplot', 'ggplot']

installed_packages = {}
failed_packages = []

for package in packages:
    success, installed_version = check_and_install_package(package)
    if success:
        installed_packages[package] = installed_version
    else:
        failed_packages.append(package)

for package in pip_only_packages:
    success, installed_version = check_and_install_package(package, use_pip=True)
    if success:
        installed_packages[package] = installed_version
    else:
        failed_packages.append(package)

print('Installed Packages:')
for package, installed_version in installed_packages.items():
    print(f'- {package}: {installed_version}')

if failed_packages:
    print('Failed Packages:')
    for package in failed_packages:
        print(f'- {package}')
else:
    print('All packages installed successfully.')

# Current project directory
PROJECT_DIR = os.getcwd()

# Your desired YAML filename
YAML_FILE = 'windbreaks.yml'

# Command to export the conda environment configuration
command = f'conda env export > "{os.path.join(PROJECT_DIR, YAML_FILE)}"'

# Execute the command
subprocess.run(command, shell=True)

