import logging
from synefind.__version__ import __version__

logging.basicConfig(
        format='%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
)

logging.getLogger("synefind").addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)
logger.info("------------------------------------------------")
logger.info("|                                              |")
logger.info("|                SYNEFIND v{}|".format(__version__.ljust(20)))
logger.info("|                                              |")
logger.info("|                                              |")
logger.info("|   'a repo is only as good as its __init__'   |")
logger.info("|                      - albert einstein       |")
logger.info("|                                              |")
logger.info("------------------------------------------------")