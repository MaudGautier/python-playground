""" From https://github.com/MaudGautier/module-not-found-shenanigans
"""

import os, site, pathlib

# Define path to pth file
pth_filename = f"{pathlib.Path(__file__).stem}.pth"
site_packages_directory = site.getsitepackages()[0]
pth_file_path = os.path.join(site_packages_directory, pth_filename)

# Add root directory to pth file
root_directory = os.path.abspath(os.path.dirname(__file__))
with open(pth_file_path, 'w') as f:
    f.write(root_directory + '\n')

print(f"Added '{root_directory}' to '{pth_file_path}'.")