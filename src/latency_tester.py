import time
import math
from socket import socket, AF_INET, SOCK_STREAM, timeout, gaierror

from logger import ss_log


class LatencyTester:
    def __init__(self, server_configs):
        if not server_configs:
            raise Exception("server_configs is null")
        self.server_configs = server_configs

    def start_test(self):
        ss_log.info(">>> Start Connection Latency Test")
        left_width = max(len(item.remarks) for item in self.server_configs)
        right_width = max(len(item.server) for item in self.server_configs)
        for index, config in enumerate(self.server_configs):
            with socket(AF_INET, SOCK_STREAM) as s:
                config_name = f"{config.remarks:<{left_width}} {config.server:>{right_width}}"
                s.settimeout(3)
                start = time.time()
                try:
                    s.connect((config.server, int(config.server_port)))
                except timeout:
                    ss_log.info(f"{config_name}: timeout")
                    config.latency = math.inf
                except ConnectionRefusedError:
                    ss_log.info(f"{config_name}: connection refused")
                    config.latency = math.inf
                except gaierror:
                    ss_log.info(f"{config_name}: server not know")
                    config.latency = math.inf
                except Exception as e:
                    ss_log.exception(e)
                    ss_log.info(f"{config_name}: test failed")
                    config.latency = math.inf
                else:
                    end = time.time()
                    ss_log.info(f"{config_name}: {(end-start)*1000:.2f} ms")
                    config.latency = (end - start) * 1000

        self.server_configs.sort(key=lambda item: item.latency)
        fastest = self.server_configs[0]
        ss_log.info(f">>> Test Finished, the lowest connection latency is:")
        ss_log.info(f">>> {fastest.remarks} {fastest.server}: {fastest.latency:.2f} ms <<<")
        return fastest
