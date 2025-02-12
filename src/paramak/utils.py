import typing
from enum import Enum

from cadquery import Workplane


class LayerType(Enum):
    GAP = "gap"
    SOLID = "solid"
    PLASMA = "plasma"


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
    workplane,
):

    for entry in instructions:
        if list(entry.keys())[0] == "spline":
            workplane = workplane.spline(listOfXYTuple=list(entry.values())[0])
        if list(entry.keys())[0] == "straight":
            workplane = workplane.polyline(list(entry.values())[0])
        if list(entry.keys())[0] == "circle":
            p0 = list(entry.values())[0][0]
            p1 = list(entry.values())[0][1]
            p2 = list(entry.values())[0][2]
            workplane = workplane.moveTo(p0[0], p0[1]).threePointArc(p1, p2)

    return workplane.close()


def create_wire_workplane_from_points(points, plane, origin=(0, 0, 0), obj=None):

    workplane = Workplane(plane, origin=origin, obj=obj)  # offset=extrusion_offset


    all_straight = all(entry[-1] == "straight" for entry in points)
    all_spline = all(entry[-1] == "spline" for entry in points)

    if all_straight:
        entry_values = [entry[:2] for entry in points[:-1]]
        result = workplane.polyline(entry_values).close()
    elif all_spline:
        entry_values = [entry[:2] for entry in points[:-1]]
        result = workplane.spline(
            entry_values, makeWire=True, tol=1e-1, periodic=True
        )  # period smooths out the connecting joint
    else:
        instructions = instructions_from_points(points)

        result = create_wire_workplane_from_instructions(
            instructions=instructions,
            workplane=workplane,
        )

    return result


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
        if item[0] == LayerType.PLASMA:
            return total_sum
        if item[0] == LayerType.GAP and i + 1 < len(radial_build) and radial_build[i + 1][0] == LayerType.PLASMA:
            return total_sum
        total_sum += item[1]
    return total_sum


def sum_up_to_plasma(radial_build):
    total_sum = 0
    for item in radial_build:
        if item[0] == LayerType.PLASMA:
            break
        total_sum += item[1]
    return total_sum


def sum_after_plasma(radial_build):
    plasma_found = False
    total_sum = 0
    for item in radial_build:
        if plasma_found:
            total_sum += item[1]
        if item[0] == LayerType.PLASMA:
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
        if item[0] == LayerType.PLASMA:
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


def is_plasma_radial_build(radial_build):
    for entry in radial_build:
        # if entry == LayerType.PLASMA:
        #     return True
        if entry[0] == LayerType.PLASMA:
            return True
    return False


def validate_divertor_radial_build(radial_build):
    if len(radial_build) != 2:
        raise ValidationError(
            f'The radial build for the divertor should only contain two entries, for example ((LayerType.GAP,10), ("lower_divertor", 10)) not {radial_build}'
        )

    if len(radial_build[0]) != 2 or len(radial_build[1]) != 2:
        raise ValidationError(
            "The radial build for the divertor should only contain tuples of length 2,, for example (LayerType.GAP,10)"
        )

    if radial_build[1][0] not in {"lower_divertor", "upper_divertor"}:
        raise ValidationError(
            f'The second entry in the radial build for the divertor should be either "lower_divertor" or "upper_divertor" not {radial_build[1][0]}'
        )

    if radial_build[0][0] != LayerType.GAP:
        raise ValidationError(
            f"The first entry in the radial build for the divertor should be a LayerType.GAP not {radial_build[0][0]}"
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
    valid_strings = {LayerType.GAP, LayerType.SOLID, LayerType.PLASMA}
    plasma_count = 0
    plasma_index = -1
    for index, item in enumerate(radial_build):
        if not isinstance(item[0], LayerType):
            raise ValidationError(f"First entry in each radial build Tuple should be a paramak.LayerType")
        if not isinstance(item[1], (int, float)):
            raise ValidationError(f"Second entry in each radial build Tuple should be a Float")
        if item[0] not in valid_strings:
            raise ValidationError(f"Invalid entry '{item[0]}' at index {index}")
        if item[1] <= 0:
            raise ValidationError(f"Non-positive value '{item[1]}' at index {index}")
        if item[0] == LayerType.PLASMA:
            plasma_count += 1
            plasma_index = index
            if plasma_count > 1:
                raise ValidationError("Multiple LayerType.PLASMA entries found")
    if plasma_count != 1:
        raise ValidationError("LayerType.PLASMA entry not found or found multiple times")
    if plasma_index == 0 or plasma_index == len(radial_build) - 1:
        raise ValidationError("LayerType.PLASMA entry must have at least one entry before and after it")
    if radial_build[plasma_index - 1][0] != LayerType.GAP or radial_build[plasma_index + 1][0] != LayerType.GAP:
        raise ValidationError("LayerType.PLASMA entry must be preceded and followed by a LayerType.GAP")


def is_lower_or_upper_divertor(radial_build):
    for item in radial_build:
        if item[0] == "lower_divertor":
            return "lower_divertor"
        if item[0] == "upper_divertor":
            return "upper_divertor"
    raise ValidationError("neither upper_divertor or lower_divertor found")


def get_plasma_value(radial_build):
    for item in radial_build:
        if item[0] == LayerType.PLASMA:
            return item[1]
    raise ValueError("LayerType.PLASMA entry not found")


def get_plasma_index(radial_build):
    for i, item in enumerate(radial_build):
        if item[0] == LayerType.PLASMA:
            return i
    raise ValueError("LayerType.PLASMA entry not found")


def get_gap_after_plasma(radial_build):
    for index, item in enumerate(radial_build):
        if item[0] == LayerType.PLASMA:
            if index + 1 < len(radial_build) and radial_build[index + 1][0] == LayerType.GAP:
                return radial_build[index + 1][1]
            else:
                raise ValueError("LayerType.PLASMA entry is not followed by a 'gap'")
    raise ValueError("LayerType.PLASMA entry not found")


def sum_after_gap_following_plasma(radial_build):
    found_plasma = False
    found_gap_after_plasma = False
    total_sum = 0

    for item in radial_build:
        if found_gap_after_plasma:
            total_sum += item[1]
        elif found_plasma and item[0] == LayerType.GAP:
            found_gap_after_plasma = True
        elif item[0] == LayerType.PLASMA:
            found_plasma = True

    if not found_plasma:
        raise ValueError("LayerType.PLASMA entry not found")
    if not found_gap_after_plasma:
        raise ValueError("LayerType.PLASMA entry is not followed by a 'gap'")

    return total_sum
