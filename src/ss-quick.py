#!/usr/bin/env python3

from gui_config_loader import ConfigLoader
from latency_tester import LatencyTester
from command_line import args

from logger import ss_log


def main(args):
    configs = ConfigLoader(args.config_file).get_server_configs()

    if args.n is not None:
        if args.n not in range(len(configs)):
            ss_log.info(f"please choose a config from 1-{len(configs)}")
            return
        config = configs[args.n - 1]
    else:
        config = LatencyTester(configs).get_fastest()
        if not config:
            return

    ss_log.info(f"\n{config}")
    # print to stdout
    print(config.to_flags())


if __name__ == "__main__":
    main(args)
