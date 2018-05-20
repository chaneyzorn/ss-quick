import sys
import uuid
import subprocess
from pathlib import Path

from logger import ss_log


class SsLocalLauncher:

    def __init__(self, config):
        self.config = config
        self._s = str(config.server)
        self._p = str(config.server_port)
        self._l = str(config.local_port)
        self._k = str(config.password)
        self._m = str(config.method)

        self.pid_file = Path(f'/tmp/ss-local:{uuid.uuid4().hex}.pid')
        self.pid = 0

    def start(self, daemon=False):
        cmd = [
            'ss-local',
            '-s', self._s,
            '-p', self._p,
            '-l', self._l,
            '-k', self._k,
            '-m', self._m,
            '-v'
        ]
        cmd += ['-f', self.pid_file] if daemon else []

        with subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        ) as process:
            try:
                self.pid = process.pid
                for line in iter(process.stdout.readline, ''):
                    sys.stdout.write(line)
            except KeyboardInterrupt:
                process.kill()
                for line in iter(process.stdout.readline, ''):
                    sys.stdout.write(line)
            except Exception as e:
                ss_log.exception(e)
                process.kill()
                process.wait()
                return
            process.wait()
            retcode = process.poll()

            if retcode == 0 and daemon:
                with self.pid_file.open('rt') as f:
                    self.pid = f.readline().strip()
                    ss_log.info(f"ss-local run in background. pid: {self.pid}")
                    ss_log.info(f"pid file: {self.pid_file}")
                return
            else:
                ss_log.info("ss-local exit with code({})".format(retcode))

    def get_ss_syslog(self):
        with subprocess.Popen(
                ['journalctl', '-f'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True
        ) as process:
            for line in iter(process.stdout.readline, ''):
                if f'ss-local[{self.pid}]' in line:
                    sys.stdout.write(line)
