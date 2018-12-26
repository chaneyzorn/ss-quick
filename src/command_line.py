from argparse import ArgumentParser

arg_parser = ArgumentParser(description="A tool to load gui-config.json for ss-local.")

arg_parser.add_argument(
    '-c', '--config-file',
    action='store',
    default='./gui-config.json',
    help="path to gui-config.json"
)
arg_parser.add_argument(
    '-n',
    action='store',
    type=int,
    default=None,
    help="choose (1-n)th config to start ss-local."
)

args = arg_parser.parse_args()


if __name__ == "__main__":
    print(args.__dict__)
