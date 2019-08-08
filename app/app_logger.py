import logging

from settings import PROJECT_ROOT


logger = logging.getLogger('app')


stream_h = logging.StreamHandler()
file_h = logging.FileHandler(PROJECT_ROOT / 'log')

stream_h.setLevel(logging.INFO)
file_h.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(levelname)s -- %(message)s')
stream_h.setFormatter(formatter)
file_h.setFormatter(formatter)


logger.addHandler(stream_h)
logger.addHandler(file_h)
logger.setLevel(logging.INFO)
