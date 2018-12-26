import json
from json import JSONDecodeError
from pathlib import Path

from logger import ss_log


class ServerConfig:
    def __init__(self, **kwargs):
        self._info = kwargs
        self.__dict__.update(kwargs)
        self.local_port = 1080

    def to_flags(self):
        flags = [
            '-s', str(self.server),
            '-p', str(self.server_port),
            '-l', str(self.local_port),
            '-k', str(self.password),
            '-m', str(self.method),
        ]
        return ' '.join(flags)

    @property
    def local_port(self):
        return self._info['local_port']

    @local_port.setter
    def local_port(self, value):
        self._info['local_port'] = value
        self.__dict__['local_port'] = value

    def __str__(self):
        info = ''
        max_width = max(len(key) for key in self._info)
        for key, value in self._info.items():
            value = '******' if key == 'password' else value
            info += f"{key:>{max_width}}: {value}\n"
        return info


class ConfigLoader:
    def __init__(self, file_path):
        config_path = Path(file_path).expanduser()
        self.config_path = config_path
        if not config_path.is_file():
            raise Exception(f"Invalid json config file: {config_path}")

        ss_log.debug("Loading config file from {}".format(config_path))
        with config_path.open('rt') as f:
            try:
                self._conf_dict = json.load(f)
            except JSONDecodeError:
                raise Exception(f"Invalid json config file: {config_path}")
            self._server_configs = None

    def get_server_configs(self):
        if not self._server_configs:
            try:
                self._server_configs = [
                    ServerConfig(**config) for config in self._conf_dict.get('configs')
                ]
            except Exception:
                raise Exception(f"Invalid json config file: {self.config_path}")
        return self._server_configs
