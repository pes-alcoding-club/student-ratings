from selenium import webdriver
from datetime import datetime, timedelta
import logging
from time import strftime, sleep

logging.basicConfig(format='%(message)s', level='INFO', datefmt=strftime("%d/%m/%Y, %H:%M:%S"))

def info(message):
    logging.info(datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
def warn(message):
    logging.warning('WARNING: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
def critical(message):
    logging.critical('CRITICAL: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
def debug(message):
    logging.debug('DEBUGGING: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + str(message))
def error(message):
    logging.error('ERROR: ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ': ' + message)
