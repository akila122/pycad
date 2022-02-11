import math
from autocad_session import channel


def extract_rectangles():
    ret = []
    cord_names = [f"{point}{value}" for point in ['a', 'b', 'c', 'd'] for value in ['x', 'y']]
    for obj in channel.session.doc.ModelSpace:
        # Test if it is a rectangle
        if "Polyline" in obj.ObjectName and obj.Closed:
            coordinates = obj.Coordinates
            if len(coordinates) != 8:
                continue
            len_a = math.dist(coordinates[:2], coordinates[2:4])
            len_b = math.dist(coordinates[2:4], coordinates[4:6])
            if (
                    len_a == math.dist(coordinates[4:6], coordinates[6:8]) and
                    len_b == math.dist(coordinates[:2], coordinates[6:8])
            ):
                cord_dict = {cord_names[i]: value for i, value in enumerate(coordinates)}
                ret.append(
                    dict(
                        len_a=len_a,
                        len_b=len_b,
                        # Floating point conversion problems, not using obj.Area
                        area=len_a * len_b,
                        perimeter=2 * len_b + 2 * len_b,
                        **cord_dict,
                    )
                )

    return ret
