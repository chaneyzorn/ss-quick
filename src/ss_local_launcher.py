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
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8') as process:
            try:
                for line in iter(process.stdout.readline, ''):
                    sys.stdout.write(line)
            except KeyboardInterrupt:
                process.kill()
                stdout, stderr = process.communicate()
                if stdout:
                    sys.stdout.write(stdout)
                if stderr:
                    sys.stderr.write(stderr)
            except Exception as e:
                ss_log.exception(e)
                process.kill()
                process.wait()
                return
            retcode = process.poll()
            if retcode is not None:
                if retcode == 0 and daemon:
                    with self.pid_file.open('rt') as f:
                        pid = f.readline().strip()
                        ss_log.info(f"ss-local run in background. pid: {pid}")
                        ss_log.info(f"pid file: {self.pid_file}")
                else:
                    ss_log.info("ss-local exit with code({})".format(retcode))
