import logging

fmt = '%(asctime)s - %(threadName)s - %(name)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)

console = logging.StreamHandler()
console.setFormatter(formatter)

file = logging.FileHandler('log.txt')
file.setLevel(logging.WARNING)
file.setFormatter(formatter)

logger = logging.getLogger('zxcs')
logger.addHandler(file)
logger.addHandler(console)
logger.setLevel(logging.DEBUG)