import asyncio
import time
import math
import socket

from logger import ss_log


class LatencyTester:
    def __init__(self, server_configs):
        if not server_configs:
            raise Exception("server_configs is null")
        self.server_configs = server_configs

    def get_fastest(self):
        return self.start_test_async()

    def start_test_async(self):
        ss_log.info(">>> Start Connection Latency Test")
        width_1 = len(f'{len(self.server_configs)}')
        width_2 = max(len(item.server) for item in self.server_configs)

        async def connect_config_server(config):
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

            ss_log.info(
                f"[{config.index:>{width_1}}] {result:<18} {config.server:>{width_2}}:{config.remarks}"
            )

        task_list = []
        for index, config in enumerate(self.server_configs):
            config.index = index + 1
            task_list.append(
                connect_config_server(config)
            )

        async def run_async():
            await asyncio.gather(*task_list)

        asyncio.run(run_async())

        rank = sorted(self.server_configs, key=lambda item: item.latency)
        fastest = rank[0]
        if fastest.status != "success":
            ss_log.info("None of configs is valid")
            return None
        ss_log.info(
            f"Test Finished, the lowest connection latency is:\n"
            f">>> {'['+str(fastest.index)+']'} {fastest.remarks} {fastest.server}: {fastest.latency:.2f} ms <<<\n"
            + str(fastest)
        )
        return fastest
