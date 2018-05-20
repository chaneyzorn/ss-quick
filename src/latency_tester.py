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
        width_1 = len(f'[{len(self.server_configs)}]')
        width_2 = max(len(item.server) for item in self.server_configs)

        for index, config in enumerate(self.server_configs):
            with socket(AF_INET, SOCK_STREAM) as s:
                s.settimeout(3)
                start = time.time()
                latency = 0
                try:
                    s.connect((config.server, int(config.server_port)))
                except timeout:
                    status = "timeout"
                except ConnectionRefusedError:
                    status = "connection refused"
                except gaierror:
                    status = "server not know"
                except Exception as e:
                    ss_log.exception(e)
                    status = "test failed"
                else:
                    status = "success"
                    latency = (time.time() - start) * 1000
                config.latency = latency or math.inf
                config.status = status
                result = latency and f"{latency:.2f} ms" or status

                ss_log.info(f"{'['+str(index)+']':>{width_1}} {result:<18} {config.server:>{width_2}}:{config.remarks}")

        rank = sorted(self.server_configs, key=lambda item: item.latency)
        fastest = rank[0]
        if fastest.status != "success":
            ss_log.info("None of configs is valid")
            return None
        ss_log.info(f">>> Test Finished, the lowest connection latency is:")
        index = self.server_configs.index(fastest)
        ss_log.info(f">>> {'['+str(index)+']'} {fastest.remarks} {fastest.server}: {fastest.latency:.2f} ms <<<")
        return fastest
