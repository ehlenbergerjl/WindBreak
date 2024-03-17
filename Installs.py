import subprocess
from importlib.metadata import version, PackageNotFoundError


def install_package_with_conda(package):
    try:
        subprocess.check_call(['conda', 'install', '-y', package])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install '{package}' using conda.")
        return False


def install_package_with_pip(package):
    try:
        subprocess.check_call(['python', '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install '{package}' using pip.")
        return False


def is_package_installed(package):
    try:
        version(package)
        return True
    except PackageNotFoundError:
        return False


def check_and_install_package(package, use_pip=False):
    if is_package_installed(package):
        print(f"'{package}' is already installed.")
    else:
        print(f"'{package}' is not installed. Installing...")
        if use_pip:
            success = install_package_with_pip(package)
        else:
            success = install_package_with_conda(package)
            if not success:
                success = install_package_with_pip(package)
        if success:
            print(f"Successfully installed '{package}'.")
        else:
            print(f"Failed to install '{package}'.")


packages = ['matplotlib', 'numpy', 'pandas', 'pygal', 'ipyleaflet']

pip_only_packages = ['geopandas', 'rasterstats', 'geoplot', 'ggplot']

for package in packages:
    check_and_install_package(package)

for package in pip_only_packages:
    check_and_install_package(package, use_pip=True)

subprocess.run('conda env export > "%USERPROFILE%/windbreaks.yml"', shell=True)