import os
from pathlib import Path

"""
Logging is used to track events that happen when software runs. It helps in debugging, monitoring, and understanding how your application behaves.
"""
import logging

"""
logging.basicConfig() sets up logging configuration.
level=logging.INFO ensures only INFO and above logs are shown.
format='[%(asctime)s]: %(message)s:' adds timestamps to logs.
Logging is better than print statements for debugging and tracking.
"""
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")


"""
DEFINING THE LIST OF FILES TO CREATE:
1. __init__.py:
Marks a directory as a Python package → Without it, Python won't recognize the folder as a package.
Allows importing modules from the package → E.g., from mypackage import mymodule.
Can run initialization code → E.g., setting up configs or importing submodules.

When Do You Need __init__.py?
For Package Imports: If you want to treat a folder as a package and import from it.
For Subdirectory Imports: If the module is in a nested folder, Python won’t recognize it as a package without __init__.py.

2. helper.py:
Here we will write all the functionalities like extract info, download the huggingface embedding model, etc 

3. prompt.py:
Inside this we will write the prompt which we will feed to the LLM

4. setup.py:
Setup where we will define our dependencies from src folder

5. trials.ipynb:
The Jupyter Notebook where we will try first before writing everything down in setup.py
"""

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # if filedir is not none then create the dir
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating Directory: {filedir} for the file {filename}")

    # if file exists and the content of the file is 0 then create
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} already exist")
