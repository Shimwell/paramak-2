Spherical Tokamak
=================

- This is characterized by a blanket that only goes around the outboard sides of the plasma and a center column that has no inboard breeding.

Spherical tokamak
-----------------

- The spherical_tokamak function provides a parametric tokamak shaped reactor.
- This is characterized by a blanket that only goes around the outboard sides of the plasma.
- This reactor allows for a separate vertical and radial build which allows different thickness layers in the blanket. 

.. cadquery::
    :gridsize: 0
    :select: result
    :color: #00cd00
    :width: 100%
    :height: 600px

    import paramak

    result = paramak.spherical_tokamak(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        vertical_build=[
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 120),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 700),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 30),
            (paramak.LayerType.SOLID, 15),
        ],
        rotation_angle=180,
        triangularity=0.55,
    ).toCompound()

.. code-block:: python

    import paramak

    result = paramak.spherical_tokamak(
        radial_build=[
                (paramak.LayerType.GAP, 10),
                (paramak.LayerType.SOLID, 50),
                (paramak.LayerType.SOLID, 10),
                (paramak.LayerType.GAP, 50),
                (paramak.LayerType.PLASMA, 300),
                (paramak.LayerType.GAP, 60),
                (paramak.LayerType.SOLID, 10),
                (paramak.LayerType.SOLID, 60),
                (paramak.LayerType.SOLID, 10),
        ],
        vertical_build=[
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 120),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 700),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 30),
            (paramak.LayerType.SOLID, 15),
        ],
        rotation_angle=180,
        triangularity=0.55,
    )

    result.save(f"spherical_tokamak_minimal.step")


Spherical tokamak from plasma
-----------------------------

- The spherical_tokamak_from_plasma function provides a parametric tokamak shaped reactor.
- This reactor requires minimal arguments to create as it keeps the vertical build of the blanket layers the same thickness as the radial build.


.. cadquery::
    :gridsize: 0
    :select: result
    :color: #00cd00
    :width: 100%
    :height: 600px

    import paramak
    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 20),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 20),
            (paramak.LayerType.SOLID, 120),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2,
        triangularity=0.55,
        rotation_angle=90,
    ).toCompound()


.. code-block:: python

    import paramak
    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 20),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 20),
            (paramak.LayerType.SOLID, 120),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2,
        triangularity=0.55,
        rotation_angle=90,
    )
    result.save('reactor.step')


Spherical tokamak with divertor
-------------------------------

- Reactors support adding additional extra intersect shapes that can be_divertor.
- This example adds a divertor to a spherical_tokamak_from_plasma reactor.

.. cadquery::
    :gridsize: 0
    :select: result
    :color: #00cd00
    :width: 100%
    :height: 600px

    from cadquery import Workplane

    # makes a rectangle that overlaps the lower blanket under the plasma
    # the intersection of this and the layers will form the lower divertor
    points = [(200, -700), (200, 0), (300, 0), (300, -700)]
    divertor_lower = Workplane('XZ', origin=(0,0,0)).polyline(points).close().revolve(180)
    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2,
        triangularity=0.55,
        rotation_angle=180,
        extra_intersect_shapes=[divertor_lower]
    ).toCompound()


.. code-block:: python

    from cadquery import Workplane

    # makes a rectangle that overlaps the lower blanket under the plasma
    # the intersection of this and the layers will form the lower divertor
    points = [(200, -700), (200, 0), (300, 0), (300, -700)]
    divertor_lower = Workplane('XZ', origin=(0,0,0)).polyline(points).close().revolve(180)
    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2,
        triangularity=0.55,
        rotation_angle=180,
        extra_intersect_shapes=[divertor_lower]
    )
    result.save('reactor.step')

Spherical tokamak with poloidal field coils
-------------------------------------------

- All reactors support adding a sequence of CadQuery shapes (e.g. workplanes) to the reactor using the extra_cut_shapes argument
- This example adds PF coils to a spherical_tokamak_from_plasma reactor but and other reactor would also work.


.. cadquery::
    :gridsize: 0
    :select: result
    :color: #00cd00
    :width: 100%
    :height: 600px

    import paramak

    extra_cut_shapes = []
    for case_thickness, height, width, center_point in zip(
        [10, 15, 15, 10], [20, 50, 50, 20], [20, 50, 50, 20],
        [(500, 300), (560, 100), (560, -100), (500, -300)]
    ):
        extra_cut_shapes.append(
            paramak.poloidal_field_coil(
                height=height, width=width, center_point=center_point, rotation_angle=270
            )
        )
        extra_cut_shapes.append(
            paramak.poloidal_field_coil_case(
                coil_height=height,
                coil_width=width,
                casing_thickness=case_thickness,
                rotation_angle=270,
                center_point=center_point,
            )
        )

    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2,
        triangularity=0.55,
        rotation_angle=270,
        extra_cut_shapes=extra_cut_shapes,
    ).toCompound()


.. code-block:: python

    import paramak

    extra_cut_shapes = []
    for case_thickness, height, width, center_point in zip(
        [10, 15, 15, 10], [20, 50, 50, 20], [20, 50, 50, 20],
        [(500, 300), (560, 100), (560, -100), (500, -300)]
    ):
        extra_cut_shapes.append(
            paramak.poloidal_field_coil(
                height=height, width=width, center_point=center_point, rotation_angle=270
            )
        )
        extra_cut_shapes.append(
            paramak.poloidal_field_coil_case(
                coil_height=height,
                coil_width=width,
                casing_thickness=case_thickness,
                rotation_angle=270,
                center_point=center_point,
            )
        )

    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2,
        triangularity=0.55,
        rotation_angle=270,
        extra_cut_shapes=extra_cut_shapes,
    )

    result.save(f"spherical_tokamak_from_plasma_with_pf_magnets.step")


Spherical tokamak with toroidal field coils
-------------------------------------------

- In a similar way to adding poloidal field coils one can also add toroidal field coils by making use of the extra_cut_shapes argument.
- All reactors support adding a sequence of CadQuery shapes (e.g. workplanes) to the reactor using the extra_cut_shapes argument
- This example adds TF coils to a spherical_tokamak_from_plasma reactor but and other reactor would also work.
- Also these are rectangle shaped TF coils but other shapes are also available.


.. cadquery::
    :gridsize: 0
    :select: result
    :color: #00cd00
    :width: 100%
    :height: 600px

    import paramak

    tf_style_1 = paramak.toroidal_field_coil_rectangle(
        horizontal_start_point = (10, 520),
        vertical_mid_point = (600, 0),
        thickness = 50,
        distance = 40,
        rotation_angle = 180,
        with_inner_leg = True,
        azimuthal_placement_angles = [0, 30, 60, 90, 120, 150, 180],
    )

    result1 = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 70),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2.5,
        rotation_angle=180,
        triangularity=0.55,
        extra_cut_shapes=[tf_style_1]
    ).toCompound().translate((700, 0, 0))

    tf_style_2 = paramak.toroidal_field_coil_princeton_d(
        r1=5,
        r2=610,
        azimuthal_placement_angles = [0, 30, 60, 90, 120, 150, 180],
        rotation_angle = 180,
        thickness = 50,
        distance = 40
    )

    result2 = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 70),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2.5,
        rotation_angle=180,
        triangularity=0.55,
        extra_cut_shapes=[tf_style_2]
    ).toCompound().translate((-700, 0, 0))

    import cadquery as cq
    result = cq.Assembly()
    result.add(result1)
    result.add(result2)
    result = result.toCompound()


.. code-block:: python

    import paramak

    tf_style_1 = paramak.toroidal_field_coil_rectangle(
        horizontal_start_point = (10, 520),
        vertical_mid_point = (600, 0),
        thickness = 50,
        distance = 40,
        with_inner_leg = True,
        rotation_angle = 180,
        azimuthal_placement_angles = [0, 30, 60, 90, 120, 150, 180],
    )

    result = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 70),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2.5,
        rotation_angle=180,
        triangularity=0.55,
        extra_cut_shapes=[tf_style_1]
    )

    result.save(f"spherical_tokamak_with_rectangular_tf.step")

    tf_style_2 = paramak.toroidal_field_coil_princeton_d(
        r1=5,
        r2=610,
        azimuthal_placement_angles = [120, 150, 180],
        rotation_angle = 180,
        thickness = 50,
        distance = 40
    )

    result2 = paramak.spherical_tokamak_from_plasma(
        radial_build=[
            (paramak.LayerType.GAP, 70),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        elongation=2.5,
        rotation_angle=180,
        triangularity=0.55,
        extra_cut_shapes=[tf]
    )

    result2.save(f"spherical_tokamak_with_princeton_tf.step")


Spherical tokamak with negative triangularity
---------------------------------------------

- The triangularity argument can be set to a negative value to make a plasma with a negative triangularity.
- This example makes a spherical tokamak with a negative but this would work on any reactor.

.. cadquery::
    :gridsize: 0
    :select: result
    :color: #00cd00
    :width: 100%
    :height: 600px

    import paramak

    result = paramak.spherical_tokamak(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 40),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        vertical_build=[
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 80),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 700),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 40),
            (paramak.LayerType.SOLID, 15),
        ],
        rotation_angle=180,
        triangularity=-0.55,
    ).toCompound()

.. code-block:: python

    import paramak

    result = paramak.spherical_tokamak(
        radial_build=[
            (paramak.LayerType.GAP, 10),
            (paramak.LayerType.SOLID, 50),
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 60),
            (paramak.LayerType.SOLID, 10),
        ],
        vertical_build=[
            (paramak.LayerType.SOLID, 15),
            (paramak.LayerType.SOLID, 80),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 700),
            (paramak.LayerType.GAP, 60),
            (paramak.LayerType.SOLID, 10),
            (paramak.LayerType.SOLID, 40),
            (paramak.LayerType.SOLID, 15),
        ],
        rotation_angle=180,
        triangularity=-0.55,
    )
    result.save(f"spherical_tokamak_minimal.step")
