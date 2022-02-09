import argparse
import inspect
import math
from pyautocad import Autocad, aDouble

import logging

logger = logging.getLogger(__name__)

session = None

# Action definitions, please use typing annotations for better CLI support e.g. name:<type>


def draw_square(start_x: float = 0, start_y: float = 0, size: float = 100):
    square_cords = aDouble(
        start_x, start_y,
        start_x + size, start_y,
        start_x + size, start_y + size,
        start_x, start_y + size,
    )
    diagonal_cords = aDouble(
        start_x, start_y,
        start_x + size, start_y + size,
    )
    square = session.model.AddLightWeightPolyline(square_cords)
    square.Closed = True
    session.model.AddLightWeightPolyline(diagonal_cords)


def extract_rectangles():
    ret = []
    cord_names = [f"{point}{value}" for point in ['a', 'b', 'c', 'd'] for value in ['x', 'y']]
    for obj in session.doc.ModelSpace:
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
                        perimeter=obj.Length,
                        **cord_dict,
                    )
                )

    return ret


ACTIONS = [draw_square, extract_rectangles]

# Build parser, so it can be interactively queried for --help
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help='actions', dest='action')
for action in ACTIONS:
    if not callable(action):
        continue
    action_parser = subparser.add_parser(action.__name__)
    spec = inspect.getfullargspec(action)
    for i, arg in enumerate(spec.args):
        try:
            default = spec.defaults[i]
            required = False
        except IndexError:
            default = None
            required = True
        _type = spec.annotations.get(arg, None)
        action_parser.add_argument(f"{'-' if required else '--'}{arg}", default=default, type=_type, required=required)


def main():
    global session

    args = parser.parse_args()
    action_to_run = None

    for a in ACTIONS:
        if a.__name__ == args.action:
            action_to_run = a
            break

    if not action_to_run:
        logger.error("Invalid setup.")
        return
    session = Autocad(create_if_not_exists=False)
    try:
        session.prompt("Python trying to connect...")
    except OSError:
        logger.error("Could not connect to the AUTOCAD process. Please start AUTOCAD before running the script.")
        return
    session.prompt("Python connected!")

    kwargs = {k: v for k, v in args.__dict__.items() if k != "action"}
    x = action_to_run(**kwargs)
    print(x)
    session.prompt(f"Action {action_to_run.__name__} done!")



if __name__ == '__main__':
    main()
