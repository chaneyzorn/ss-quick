#!/usr/bin/env python3

from gui_config_loader import ConfigLoader
from latency_tester import LatencyTester
from command_line import args

from logger import ss_log


def main(args):
    config_loader = ConfigLoader(args.config_file)
    configs = config_loader.get_server_configs()

    if args.n is not None:
        index = args.n
        if index not in range(len(configs)):
            ss_log.info(f"please choose a config from 1-{len(configs)}")
            return
        config = configs[index]
    else:
        config = LatencyTester(configs).get_fastest()
        if not config:
            return

    # print to stdout
    print(config.to_flags())


if __name__ == "__main__":
    main(args)
