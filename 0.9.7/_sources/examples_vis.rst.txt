
Visualization options
=====================

The reactors (cadquery.Assembly objects) and components (cadquery.Workplane objects) can be visualized in a number of ways.
First option is to export them to STEP, BREP or STL file then open the file with your favorite CAD software for example `FreeCAD <https://www.freecad.org/>`_.
See the `CadQuery documentation on saving <https://cadquery.readthedocs.io/en/latest/importexport.html#exporting-step>`_ for more information.
Other options include the built in visualization tools in CadQuery

.. code-block:: python

    from cadquery.vis import show
    show(result)  # where result is the returned reactor or component object

Jupyter_cadquery package can be installed (pip install jupyter-cadquery) which allows for interactive 3D visualization in a web browser.
This package can also be used to export portable html files with the 3D visualization.

.. code-block:: python

    # pip install jupyter_cadquery
    # might needed to downgrade pip with ... python -m pip  install pip==24.0
    from jupyter_cadquery import show
    view = show(result)  # where result is the returned reactor or component object
    view.export_html("3d.html")
