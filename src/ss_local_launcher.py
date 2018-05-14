import sys
import uuid
import subprocess
from pathlib import Path


class SsLocalLauncher:

    def __init__(self, config):
        self.config = config
        self._s = str(config.server)
        self._p = str(config.server_port)
        self._l = str(config.local_port)
        self._k = str(config.password)
        self._m = str(config.method)

        self.pid_file = Path(f'/tmp/ss-local:{uuid.uuid4().hex}.pid')

    def __enter__(self):
        self._start()
        with self.pid_file.open('rt') as f:
            self.pid = f.readline().strip()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        subprocess.call(['kill', self.pid])
        self.pid_file.unlink()

    def _start(self):
        subprocess.run([
            'ss-local',
            '-s', self._s,
            '-p', self._p,
            '-l', self._l,
            '-k', self._k,
            '-m', self._m,
            '-f', self.pid_file,
            '-v'
        ], check=True)

    def get_ss_syslog(self):
        with subprocess.Popen(
            ['journalctl', '-f'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding='utf-8'
        ) as process:
            for line in iter(process.stdout.readline, ''):
                if f'ss-local[{self.pid}]' in line:
                    sys.stdout.write(line)
