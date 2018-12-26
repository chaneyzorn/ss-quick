#!/usr/bin/env python3

from gui_config_loader import ConfigLoader
from ss_local_launcher import SsLocalLauncher
from latency_tester import LatencyTester
from command_line import args

from logger import ss_log


def start_ss_proxy(config, args):
    ss_log.debug(f"Start ss-local with following config: \n{config}")
    ss_proxy = SsLocalLauncher(config)
    ss_proxy.start(daemon=args.daemon)


def main(args):
    config_loader = ConfigLoader(args.config_file)
    configs = config_loader.get_server_configs()

    if args.n is not False:
        index = args.n
        if index not in range(len(configs)):
            raise Exception(f"please choose a config from 1-{len(configs)}")
        config = configs[index - 1]
    elif args.fastest:
        config = LatencyTester(configs).get_fastest()
        if not config:
            return
    else:
        ss_log.debug("Invalid Arguments.")
        return

    config.local_port = args.local_port
    if args.flags:
        print(config.to_flags())
    else:
        start_ss_proxy(config, args)


if __name__ == "__main__":
    main(args)
