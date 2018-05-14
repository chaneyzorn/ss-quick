#!/usr/bin/env python3

from gui_config_loader import ConfigLoader
from ss_local_launcher import SsLocalLauncher
from latency_tester import LatencyTester
from command_line import arg_parser

from logger import ss_log


def start_ss_proxy(config):
    ss_log.info(f"Start ss-local with following config: \n{config}")
    try:
        with SsLocalLauncher(config) as ss_proxy:
            ss_proxy.get_ss_syslog()
    except KeyboardInterrupt:
        ss_log.info("ss-local closed gracefully")


def main(args):
    config_loader = ConfigLoader(args.config_file)
    configs = config_loader.get_server_configs()

    if args.fastest:
        fastest_config = LatencyTester(configs).start_test()
        fastest_config.local_port = args.local_port
        start_ss_proxy(fastest_config)
    elif args.n:
        index = args.n - 1
        if index not in range(len(configs)):
            raise Exception(f"please choose a config from 1-{len(configs)}")
        config = configs[index]
        config.local_port = args.local_port
        start_ss_proxy(config)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args)
