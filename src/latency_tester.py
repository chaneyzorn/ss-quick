import asyncio
import sys
import time
import math
import socket

from logger import ss_log


class LatencyTester:
    def __init__(self, server_configs):
        if not server_configs:
            raise Exception("server_configs is null")
        self.server_configs = server_configs

        self.server_count = len(self.server_configs)
        self.max_index_len = len(f'{self.server_count}')
        self.max_name_len = max(len(item.server) for item in self.server_configs)

        self.write = sys.stderr.write
        self.flush = sys.stderr.flush

    def get_fastest(self):
        return asyncio.run(self.start_test_async())

    async def connect_test(self, config):
        start = time.time()
        latency = 0
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(
                config.server, int(config.server_port)
            ), timeout=3)
            status = "success"
            latency = (time.time() - start) * 1000

            writer.close()
            await writer.wait_closed()
        except asyncio.TimeoutError as e:
            status = "timeout"
        except socket.gaierror as e:
            status = "server not know"
        except OSError as e:
            if e.errno == 101:
                status = "unreachable"
            else:
                ss_log.exception(e)
                status = "test failed"
        except Exception as e:
            ss_log.exception(e)
            status = "test failed"

        config.latency = latency or math.inf
        config.status = status
        result = latency and f"{latency:.2f} ms" or status

        self._refresh_report(config, result)

    async def start_test_async(self):
        task_list = []
        ss_log.info("Start Connection Latency Test")
        for index, config in enumerate(self.server_configs):
            config.index = index
            task_list.append(self.connect_test(config))
            self.write(
                f"[{config.index + 1:>{self.max_index_len}}] {'connecting...':<18} "
                f"{config.server:>{self.max_name_len}}:{config.remarks}\n"
            )
        self.flush()

        await asyncio.gather(*task_list)

        rank = sorted(self.server_configs, key=lambda item: item.latency)
        fastest = rank[0]
        if fastest.status != "success":
            ss_log.info("None of configs is valid")
            return None
        ss_log.info(
            f"Test Finished, the lowest connection latency is:\n"
            f"{'['+str(fastest.index)+']'} {fastest.remarks} "
            f"{fastest.server}: {fastest.latency:.2f} ms"
        )
        return fastest

    def _refresh_report(self, config, result):
        line_count = self.server_count - config.index
        self.write(f"\033[{line_count}A" + "\r")
        self.write(f"[{config.index + 1:>{self.max_index_len}}] {result:<18} ")
        self.write(f"\033[{line_count}B" + "\r")
        self.flush()
