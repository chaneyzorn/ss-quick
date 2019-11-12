#!/usr/bin/env python3

from ss_quick.gui_config_loader import ConfigLoader
from ss_quick.latency_tester import LatencyTester
from ss_quick.command_line import args

from ss_quick.logger import ss_log


def main():
    cli(args)


def cli(args):
    configs = ConfigLoader(args.config_file).get_server_configs()

    if args.n is not None:
        if args.n not in range(len(configs)):
            ss_log.info(f"please choose a config from 1-{len(configs)}")
            return
        config = configs[args.n - 1]
    else:
        config = LatencyTester(configs).get_fastest(args.debug)
        if not config:
            return

    ss_log.info(f"\n{config}")
    # print to stdout
    if args.uri:
        print(config.to_uri())
    else:
        print(config.to_flags())


if __name__ == "__main__":
    main()
