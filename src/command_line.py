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
    default=False,
    help="choose (0-n)th config to start ss-local."
)
arg_parser.add_argument(
    '--fastest',
    action='store_true',
    default=False,
    help="start ss-local with the fastest one."
)
arg_parser.add_argument(
    '-l', '--local-port',
    action='store',
    type=int,
    default=1080,
    help="port number of your local server."
)
arg_parser.add_argument(
    '-d', '--daemon',
    action='store_true',
    default=False,
    help="run in the background."
)
arg_parser.add_argument(
    '--flags',
    action='store_true',
    default=False,
    help="only print required flags of ss-local to stdout."
)
arg_parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    default=False,
    help="make the operation more talkative."
)

args = arg_parser.parse_args()


if __name__ == "__main__":
    print(args.__dict__)
