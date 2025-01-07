Install
=======


Paramak is distributed via `PyPI <https://pypi.org/project/paramak/>`_ and `Conda Forge <https://anaconda.org/conda-forge/paramak>`_ can be installed using pip or Conda / Mamba.


Install from PyPI using pip

.. code-block:: bash

   python -m pip install paramak

Install from Conda Forge using Conda or Mamba

.. code-block:: bash

   mamba install -c conda-forge paramak
   conda install -c conda-forge paramak



Prerequisites
-------------

It is recommended to create a virtual environment to install Paramak into.

This can be done using the `venv module <https://docs.python.org/3/library/venv.html>`_ in or a Conda or Mamba environment.

To create a virtual environment using the venv module

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install python3-virtualenv
   python -m venv paramak-venv
   source paramak-venv/bin/activate

To create a virtual environment using Conda or Mamba

First install Miniconda or Anaconda, or Miniforge

* `Miniforge <https://github.com/conda-forge/miniforge>`_ recommended as it includes Mamba 
* `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_
* `Anaconda <https://www.anaconda.com/>`_

Once you have a version of Mamba or Conda installed then proceed with creating the virtual environment.

Create a new environment with mamba and your preferred python version then activate the new environment.

.. code-block:: bash

   mamba create --name paramak_env python=3.12
   mamba activate paramak_env

Or with Conda

.. code-block:: bash

   conda create --name paramak_env python=3.12
   conda activate paramak_env


Developer Installation
----------------------

If you want to contribute to Paramak or then you might want to install the
package in a more dynamic manner so that your changes to the code are readily
available.

Create a new Venv, Conda or Mamba virtual environment and activate the
environment as covered in the installation procedure above

Then clone the repository

.. code-block:: bash

   git clone https://github.com/fusion-energy/paramak.git

Navigate to the paramak repository and within the terminal install the paramak
package and the dependencies using pip with e -e (developer option).

.. code-block:: bash

   cd paramak
   python -m pip install -e .
