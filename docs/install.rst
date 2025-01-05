Install
=======

Paramak is distributed via `PyPI <https://pypi.org/project/paramak/>`_ and can be installed using pip.

.. code-block:: bash

   pip install paramak


.. Prerequisites
.. -------------

.. To use of Paramak you will need Python 3 installed using Miniconda or Anaconda, or Miniforge

.. * `Miniforge <https://github.com/conda-forge/miniforge>`_ recommended as it includes Mamba 
.. * `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_
.. * `Anaconda <https://www.anaconda.com/>`_



.. Once you have a version of Mamba or Conda installed then proceed with the Paramak specific steps.


.. Install (mamba)
.. ---------------

.. This is the recommended method as it installs all the dependencies and Mamba is faster and requires less RAM than the pure Conda method.

.. Create a new environment (with your preferred python version).

.. .. code-block:: bash

..    mamba create --name paramak_env python=3.11


.. Then activate the new environment.

.. .. code-block:: bash

..    mamba activate paramak_env


.. Then install the Paramak.

.. .. code-block:: bash

..    mamba install -c conda-forge paramak

.. Now you should be ready to import paramak from your new python environment.

.. Install (conda)
.. ---------------

.. Create a new environment (with your preferred python version).

.. .. code-block:: bash

..    conda create --name paramak_env python=3.11


.. Then activate the new environment.

.. .. code-block:: bash

..    conda activate paramak_env

.. Then install the Paramak.

.. .. code-block:: bash

..    mamba install -c conda-forge paramak

.. Now you should be ready to import paramak from your new python environment.



Developer Installation
----------------------

If you want to contribute to the paramak or then you might want to install the
package in a more dynamic manner so that your changes to the code are readily available.

Download and install MiniConda, create a new python environment and activate the
environment as covered in the installation procedure above.

Then clone the repository

.. code-block:: bash

   git clone https://github.com/fusion-energy/paramak.git

Navigate to the paramak repository and within the terminal install the paramak
package and the dependencies using pip with e -e (developer option).

.. code-block:: bash

   cd paramak
   pip install -e .
