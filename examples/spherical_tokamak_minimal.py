from pathlib import Path

from cad_to_dagmc import CadToDagmc
from example_util_functions import transport_particles_on_h5m_geometry

import paramak

my_reactor = paramak.spherical_tokamak(
    radial_builds=[
        [
            (paramak.LayerType.GAP, 10),
            (LayerType.SOLID, 50),
            (LayerType.SOLID, 15),
            (paramak.LayerType.GAP, 50),
            (paramak.LayerType.PLASMA, 300),
            (paramak.LayerType.GAP, 60),
            (LayerType.SOLID, 40),
            (LayerType.SOLID, 60),
            (LayerType.SOLID, 10),
        ]
    ],
    vertical_build=[
        (LayerType.SOLID, 15),
        (LayerType.SOLID, 80),
        (LayerType.SOLID, 10),
        (paramak.LayerType.GAP, 50),
        (paramak.LayerType.PLASMA, 700),
        (paramak.LayerType.GAP, 60),
        (LayerType.SOLID, 10),
        (LayerType.SOLID, 40),
        (LayerType.SOLID, 15),
    ],
    rotation_angle=180,
    triangularity=-0.55,
)
my_reactor.save(f"spherical_tokamak_minimal.step")


my_model = CadToDagmc()
material_tags = ["mat1"] * 6
my_model.add_cadquery_object(cadquery_object=my_reactor, material_tags=material_tags)
my_model.export_dagmc_h5m_file(min_mesh_size=3.0, max_mesh_size=20.0)

h5m_filename = "dagmc.h5m"
flux = transport_particles_on_h5m_geometry(
    h5m_filename=h5m_filename,
    material_tags=material_tags,
    nuclides=["H1"] * len(material_tags),
    cross_sections_xml="tests/cross_sections.xml",
)
assert flux > 0.0
