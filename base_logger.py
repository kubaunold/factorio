import logging

logger = logging
logging.basicConfig(filename="log.log",
                        level=logging.INFO,
                        filemode='w',
                        format='%(asctime)s | %(levelname)s | %(message)s')