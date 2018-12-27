from logging import getLogger, INFO, basicConfig

basicConfig(
    level=INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
ss_log = getLogger("ss-up")
