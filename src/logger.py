from command_line import args
from logging import getLogger, INFO, DEBUG, basicConfig

basicConfig(
    level=DEBUG if args.verbose else INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m-%d %H:%M:%S'
)
ss_log = getLogger("ss-up")
