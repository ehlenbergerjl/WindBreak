import os
from nbformat import read, write


def update_notebook_kernels():
    """
   This script updates the kernel metadata of each Jupyter notebook in and below the directory
   it is run from. The kernel name 'WindBreaks', which should be the name of an installed
   Jupyter kernel, is set as the kernel for each notebook. Therefore, this script should be
   run after ensuring the 'WindBreaks' kernel is installed e.g., by using the
   wb_jupyter_kernel_install.py script.

   Note that is a metadata update only, no changes are made to the actual code executed
   within the Jupyter notebooks.
   """

    # Set the kernel specs
    kernelspec = {
        "display_name": "WindBreaks",
        "language": "python",
        "name": "WindBreaks"  # This should match the name of the installed kernel
    }

    # Walk the current directory
    for dirpath, _, filenames in os.walk(os.getcwd()):
        # Find all .ipynb files
        for filename in filenames:
            if filename.endswith('.ipynb'):
                filepath = os.path.join(dirpath, filename)

                # Open the notebook file
                with open(filepath, 'r') as f:
                    nb = read(f, 4)

                # Set the kernel specs in the metadata
                nb.metadata.kernelspec = kernelspec

                # Save the notebook file
                with open(filepath, 'w') as f:
                    write(nb, f)

                print(f'Successfully updated "{filepath}" to use the WindBreaks kernel.')


# Call the function
update_notebook_kernels()
#%%
