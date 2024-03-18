import os
import subprocess


def create_jupyter_kernel(env_name, kernel_name):
    '''
    Creates a Jupyter kernel for a given Conda environment.

    Args:
        env_name (str): The name of the Conda environment.
        kernel_name (str): The name to give to the new Jupyter kernel.

    Returns:
        bool: True if the kernel was created successfully, False otherwise.
    '''
    try:
        # Generate the command to create the Jupyter kernel
        command = f'conda activate {env_name} && ipython kernel install --name "{kernel_name}" --user'

        # Execute the command
        subprocess.check_call(command, shell=True)

        # If no exceptions were thrown, the kernel was created successfully
        return True
    except subprocess.CalledProcessError:
        # If an exception was thrown, the kernel was not created successfully
        print(f'Failed to create a Jupyter kernel for the "{env_name}" Conda environment.')
        return False


# Use the function to create a Jupyter kernel for the "WindBreaks" Conda environment
create_jupyter_kernel('WindBreaks', 'WindBreaks')
