'''setup selenium'''

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_selenium():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROME_DRIVER_PATH"), chrome_options=options)
    return driver


_all_ = ['get_selenium']
