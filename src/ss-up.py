#!/usr/bin/env python3

from gui_config_loader import ConfigLoader
from ss_local_launcher import SsLocalLauncher
from latency_tester import LatencyTester
from command_line import arg_parser

from logger import ss_log


def start_ss_proxy(config):
    ss_log.info(f"Start ss-local with following config: \n{config}")
    ss_proxy = SsLocalLauncher(config)
    ss_proxy.start()


def main(args):
    config_loader = ConfigLoader(args.config_file)
    configs = config_loader.get_server_configs()

    if args.n:
        index = args.n
        if index not in range(len(configs)):
            raise Exception(f"please choose a config from 1-{len(configs)}")
        config = configs[index]
        config.local_port = args.local_port
        start_ss_proxy(config)
    elif args.fastest:
        fastest_config = LatencyTester(configs).start_test()
        if not fastest_config:
            return
        fastest_config.local_port = args.local_port
        start_ss_proxy(fastest_config)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args)
