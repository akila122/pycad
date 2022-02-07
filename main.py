import argparse
import inspect
from pyautocad import Autocad, aDouble

import logging

logger = logging.getLogger(__name__)

session = None

# Action definitions, please use typing annotations for better CLI support e.g. name:<type>


def draw_square(start_x: float = 0, start_y: float = 0, size: float = 100):
    square = aDouble(
        start_x, start_y, 0,
        start_x + size, start_y, 0,
        start_x + size, start_y + size, 0,
        start_x, start_y + size, 0,
        start_x, start_y, 0,
    )
    diagonal = aDouble(
        start_x, start_y, 0,
        start_x + size, start_y + size, 0
    )
    session.model.AddPolyline(square)
    session.model.AddPolyline(diagonal)


ACTIONS = [draw_square]

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
    action_to_run(**kwargs)
    session.prompt(f"Action {action_to_run.__name__} done!")


if __name__ == '__main__':
    main()
