import argparse
import inspect
import actions
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Build parser, so it can be interactively queried for --help
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help='actions', dest='action')
for action in actions.ACTIONS:
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
    args = parser.parse_args()
    action_to_run = None

    for a in actions.ACTIONS:
        if a.__name__ == args.action:
            action_to_run = a
            break

    if not action_to_run:
        pprint("Invalid setup.")
        return

    kwargs = {k: v for k, v in args.__dict__.items() if k != "action"}
    result = action_to_run(**kwargs)
    if result:
        pprint(result)


if __name__ == '__main__':
    main()
