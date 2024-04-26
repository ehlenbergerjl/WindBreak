import nbformat as nbf


def correct_notebook(file_name):
    with open(file_name, 'r') as nb_file:
        nb = nbf.read(nb_file, nbf.NO_CONVERT)

    for cell in nb.cells:
        if 'execution_count' not in cell:
            cell['execution_count'] = None

    with open(file_name, 'w') as nb_file:
        nbf.write(nb, nb_file)


correct_notebook('Assignment2_refactor.ipynb')

# %%

# %%
