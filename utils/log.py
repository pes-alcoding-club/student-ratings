from datetime import datetime, timedelta
import logging
from time import strftime

logging.basicConfig(format='%(message)s', level='DEBUG', datefmt=strftime("%d/%m/%Y, %H:%M:%S"))

def info(message):
    logging.info(datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
def warn(message):
    logging.warning('WARNING: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
def critical(message):
    logging.critical('CRITICAL: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
def debug(message):
    logging.debug(datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + str(message))
def error(message):
    logging.error('ERROR: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
