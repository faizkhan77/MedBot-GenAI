from setuptools import find_packages, setup

"""
This is setting up your project as a Python package that can be installed locally
setup.py is a script that defines the package and its dependencies.
✔️ find_packages() automatically detects Python packages inside the project.
✔️ install_requires=[] is where dependencies would go (but it’s empty here).
✔️ Running pip install . (or pip install -e .) installs the package.

If you include -e . inside requirements.txt, it means:
✔️ Editable mode installation (also called "development mode").
✔️ Any changes you make to the code will be immediately reflected without reinstallation.

Why Use -e .?
When developing a package, you don’t need to reinstall it after every change.
Useful for projects where you modify code frequently (like your chatbot).
"""

setup(
    name="GenAI Project",  # Package name
    version="0.0.0",  # Initial version
    author="Mohd Faiz Khan",
    author_email="faizkhan.net7@gmail.com",
    packages=find_packages(),  # Automatically finds all Python packages (folders with `__init__.py`)
    install_requires=[],  # List of dependencies (currently empty)
)
