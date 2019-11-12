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
arg_parser.add_argument(
    '--uri',
    action='store_true',
    default=False,
    help="print config in the form of uri to stdout."
)
arg_parser.add_argument(
    '--debug',
    action='store_true',
    default=False,
    help="print debug information."
)

args = arg_parser.parse_args()


if __name__ == "__main__":
    print(args.__dict__)
