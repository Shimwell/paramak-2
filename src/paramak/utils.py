import typing

from cadquery import Workplane


def instructions_from_points(points):
    # obtains the first two values of the points list
    XZ_points = [(p[0], p[1]) for p in points]

    # obtains the last values of the points list
    connections = [p[2] for p in points[:-1]]

    current_linetype = connections[0]
    current_points_list = []
    instructions = []
    # groups together common connection types
    for i, connection in enumerate(connections):
        if connection == current_linetype:
            current_points_list.append(XZ_points[i])
        else:
            current_points_list.append(XZ_points[i])
            instructions.append({current_linetype: current_points_list})
            current_linetype = connection
            current_points_list = [XZ_points[i]]
    instructions.append({current_linetype: current_points_list})

    if list(instructions[-1].values())[0][-1] != XZ_points[0]:
        keyname = list(instructions[-1].keys())[0]
        instructions[-1][keyname].append(XZ_points[0])
    return instructions


def create_wire_workplane_from_instructions(
    instructions,
    plane="XY",
    origin=(0, 0, 0),
    obj=None,
):
    solid = Workplane(plane, origin=origin, obj=obj)  # offset=extrusion_offset

    all_spline = all(list(entry.keys())[0] == "spline" for entry in instructions)
    if all_spline:
        entry_values = [(list(entry.values())[0]) for entry in instructions][0][:-1]
        res = solid.spline(
            entry_values, makeWire=True, tol=1e-1, periodic=True
        )  # period smooths out the connecting joint
        return res

    for entry in instructions:
        if list(entry.keys())[0] == "spline":
            solid = solid.spline(listOfXYTuple=list(entry.values())[0])
        if list(entry.keys())[0] == "straight":
            solid = solid.polyline(list(entry.values())[0])
        if list(entry.keys())[0] == "circle":
            p0 = list(entry.values())[0][0]
            p1 = list(entry.values())[0][1]
            p2 = list(entry.values())[0][2]
            solid = solid.moveTo(p0[0], p0[1]).threePointArc(p1, p2)

    return solid.close()


def create_wire_workplane_from_points(points, plane, origin=(0, 0, 0), obj=None):
    instructions = instructions_from_points(points)

    return create_wire_workplane_from_instructions(
        instructions,
        plane=plane,
        origin=origin,
        obj=obj,
    )


def rotate_solid(angles: typing.Sequence[float], solid: Workplane) -> Workplane:
    rotation_axis = {
        "X": [(-1, 0, 0), (1, 0, 0)],
        "-X": [(1, 0, 0), (-1, 0, 0)],
        "Y": [(0, -1, 0), (0, 1, 0)],
        "-Y": [(0, 1, 0), (0, -1, 0)],
        "Z": [(0, 0, -1), (0, 0, 1)],
        "-Z": [(0, 0, 1), (0, 0, -1)],
    }

    rotated_solids = []
    # Perform separate rotations for each angle
    for angle in angles:
        rotated_solids.append(solid.rotate(*rotation_axis["Z"], angle))
    solid = Workplane(solid.plane)

    # Joins the solids together
    for i in rotated_solids:
        solid = solid.union(i)
    return solid


def sum_up_to_gap_before_plasma(radial_build):
    total_sum = 0
    for i, item in enumerate(radial_build):
        if item[0] == "plasma":
            return total_sum
        if item[0] == "gap" and i + 1 < len(radial_build) and radial_build[i + 1][0] == "plasma":
            return total_sum
        total_sum += item[1]
    return total_sum


def sum_up_to_plasma(radial_build):
    total_sum = 0
    for item in radial_build:
        if item[0] == "plasma":
            break
        total_sum += item[1]
    return total_sum


def sum_after_plasma(radial_build):
    plasma_found = False
    total_sum = 0
    for item in radial_build:
        if plasma_found:
            total_sum += item[1]
        if item[0] == "plasma":
            plasma_found = True
    return total_sum


class ValidationError(Exception):
    pass


def sum_before_after_plasma(vertical_build):
    before_plasma = 0
    after_plasma = 0
    plasma_value = 0
    plasma_found = False

    for item in vertical_build:
        if item[0] == "plasma":
            plasma_value = item[1] / 2
            plasma_found = True
            continue
        if not plasma_found:
            before_plasma += item[1]
        else:
            after_plasma += item[1]

    before_plasma += plasma_value
    after_plasma += plasma_value

    return before_plasma, after_plasma


def create_divertor_envelope(divertor_radial_build, blanket_height, rotation_angle):
    divertor_name = is_lower_or_upper_divertor(divertor_radial_build)
    if divertor_name == "lower_divertor":
        z_value_sigh = -1
    elif divertor_name == "upper_divertor":
        z_value_sigh = 1

    points = [
        (divertor_radial_build[0][1], z_value_sigh * blanket_height, "straight"),
        (divertor_radial_build[0][1], 0, "straight"),
        (divertor_radial_build[0][1] + divertor_radial_build[1][1], 0, "straight"),
        (divertor_radial_build[0][1] + divertor_radial_build[1][1], z_value_sigh * blanket_height, "straight"),
    ]
    points.append(points[0])

    wire = create_wire_workplane_from_points(points=points, plane="XZ", origin=(0, 0, 0), obj=None)

    divertor_solid = wire.revolve(rotation_angle)
    divertor_solid.name = divertor_name
    return divertor_solid


def build_divertor_modify_blanket(outer_layers, divertor_radial_builds, blanket_rear_wall_end_height, rotation_angle):

    divertor_layers = []
    for divertor_radial_build in divertor_radial_builds:

        divertor_solid = create_divertor_envelope(divertor_radial_build, blanket_rear_wall_end_height, rotation_angle)

        # finds the intersection of the blanket and divertor rectangle envelope.
        outer_layer_envelope = outer_layers[0]
        for outer_layer in outer_layers[1:]:
            outer_layer_envelope = outer_layer_envelope.union(outer_layer)

        divertor_solid = divertor_solid.intersect(outer_layer_envelope)
        # we reapply this name as it appears to get lost and we might need it when adding to assembly
        divertor_solid.name = is_lower_or_upper_divertor(divertor_radial_build)

        # cuts the diverter out of the outer layers of the blanket
        for i, layer in enumerate(outer_layers):
            layer = layer.cut(divertor_solid)
            outer_layers[i] = layer
        divertor_layers.append(divertor_solid)
    return divertor_layers, outer_layers


def is_plasma_radial_build(radial_build):
    for entry in radial_build:
        if entry[0] == "plasma":
            return True
    return False


def extract_radial_builds(radial_build):
    # TODO more rubust method of finding if it is a single list of tupes or multiple lists
    # only one radial build so it should be a plasma based radial build
    divertor_radial_builds = []
    if isinstance(radial_build[0][0], str) and (
        isinstance(radial_build[0][1], float) or isinstance(radial_build[0][1], int)
    ):
        plasma_radial_build = radial_build
    else:
        for entry in radial_build:
            if is_plasma_radial_build(entry):
                # TODO this assumes htere is only one radial build, which needs to e checked
                plasma_radial_build = entry
            else:
                divertor_radial_builds.append(entry)

    validate_plasma_radial_build(plasma_radial_build)
    for divertor_radial_build in divertor_radial_builds:
        validate_divertor_radial_build(divertor_radial_build)
    return plasma_radial_build, divertor_radial_builds


def validate_divertor_radial_build(radial_build):
    if len(radial_build) != 2:
        raise ValidationError(
            f'The radial build for the divertor should only contain two entries, for example (("gap",10), ("lower_divertor", 10)) not {radial_build}'
        )

    if len(radial_build[0]) != 2 or len(radial_build[1]) != 2:
        raise ValidationError(
            'The radial build for the divertor should only contain tuples of length 2,, for example ("gap",10)'
        )

    if radial_build[1][0] not in {"lower_divertor", "upper_divertor"}:
        raise ValidationError(
            f'The second entry in the radial build for the divertor should be either "lower_divertor" or "upper_divertor" not {radial_build[1][0]}'
        )

    if radial_build[0][0] != "gap":
        raise ValidationError(
            f'The first entry in the radial build for the divertor should be a "gap" not {radial_build[0][0]}'
        )

    if not isinstance(radial_build[0][1], (int, float)) or not isinstance(radial_build[1][1], (int, float)):
        raise ValidationError(
            f"The thickness of the gap and the divertor should both be integers or floats, not {type(radial_build[0][1])} and {type(radial_build[1][1])}"
        )

    if radial_build[0][1] <= 0 or radial_build[1][1] <= 0:
        raise ValidationError(
            f"The thickness of the gap and the divertor should both be positive values, not {radial_build[0][1]} and {radial_build[1][1]}"
        )


def validate_plasma_radial_build(radial_build):
    # TODO should end with layer, not gap
    valid_strings = {"gap", "layer", "plasma"}
    plasma_count = 0
    plasma_index = -1
    for index, item in enumerate(radial_build):
        if not (isinstance(item[0], str) and isinstance(item[1], (int, float))):
            raise ValidationError(f"Invalid tuple structure at index {index}: {item}")
        if item[0] not in valid_strings:
            raise ValidationError(f"Invalid string '{item[0]}' at index {index}")
        if item[1] <= 0:
            raise ValidationError(f"Non-positive value '{item[1]}' at index {index}")
        if item[0] == "plasma":
            plasma_count += 1
            plasma_index = index
            if plasma_count > 1:
                raise ValidationError("Multiple 'plasma' entries found")
    if plasma_count != 1:
        raise ValidationError("'plasma' entry not found or found multiple times")
    if plasma_index == 0 or plasma_index == len(radial_build) - 1:
        raise ValidationError("'plasma' entry must have at least one entry before and after it")
    if radial_build[plasma_index - 1][0] != "gap" or radial_build[plasma_index + 1][0] != "gap":
        raise ValidationError("'plasma' entry must be preceded and followed by a 'gap'")


def is_lower_or_upper_divertor(radial_build):
    for item in radial_build:
        if item[0] == "lower_divertor":
            return "lower_divertor"
        if item[0] == "upper_divertor":
            return "upper_divertor"
    raise ValidationError("neither upper_divertor or lower_divertor found")


def get_plasma_value(radial_build):
    for item in radial_build:
        if item[0] == "plasma":
            return item[1]
    raise ValueError("'plasma' entry not found")


def get_plasma_index(radial_build):
    for i, item in enumerate(radial_build):
        if item[0] == "plasma":
            return i
    raise ValueError("'plasma' entry not found")


def get_gap_after_plasma(radial_build):
    for index, item in enumerate(radial_build):
        if item[0] == "plasma":
            if index + 1 < len(radial_build) and radial_build[index + 1][0] == "gap":
                return radial_build[index + 1][1]
            else:
                raise ValueError("'plasma' entry is not followed by a 'gap'")
    raise ValueError("'plasma' entry not found")


def sum_after_gap_following_plasma(radial_build):
    found_plasma = False
    found_gap_after_plasma = False
    total_sum = 0

    for item in radial_build:
        if found_gap_after_plasma:
            total_sum += item[1]
        elif found_plasma and item[0] == "gap":
            found_gap_after_plasma = True
        elif item[0] == "plasma":
            found_plasma = True

    if not found_plasma:
        raise ValueError("'plasma' entry not found")
    if not found_gap_after_plasma:
        raise ValueError("'plasma' entry is not followed by a 'gap'")

    return total_sum
