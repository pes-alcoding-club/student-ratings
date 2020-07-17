from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import strftime, sleep

def make_driver():
    chromeOptions = Options()
    chromeOptions.add_argument('window-size=1920x1080')
    chromeOptions.add_argument("disable-gpu")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("'--disable-setuid-sandbox'")
    #chromeOptions.add_argument('headless')
    chromeOptions.add_argument('--no-proxy-server')
    chromeOptions.add_argument("--proxy-server='direct://'")
    chromeOptions.add_argument("--proxy-bypass-list=*")
    return webdriver.Chrome(options=chromeOptions)

def load(driver):
    waiter = WebDriverWait(driver, 30)
    def _load(token, options='tag'):
        if options == 'xpath':
            return waiter.until(EC.presence_of_element_located((By.XPATH, token)))
        if options == 'tag':
            return waiter.until(EC.presence_of_element_located((By.TAG_NAME, token)))
        if options == 'text':
            return waiter.until(EC.presence_of_element_located((By.LINK_TEXT, token)))
        if options == 'class':
            return waiter.until(EC.presence_of_element_located((By.CLASS_NAME, token)))
    return _load

def load_all(driver):
    waiter = WebDriverWait(driver, 30)
    def _load_all(token, options='class'):
        if options == 'class':
            return waiter.until(EC.presence_of_all_elements_located((By.CLASS_NAME, token)))
        if options == 'xpath':
            return waiter.until(EC.presence_of_all_elements_located((By.XPATH, token)))
        if options == 'tag':
            return waiter.until(EC.presence_of_all_elements_located((By.TAG_NAME, token)))        
    return _load_all
