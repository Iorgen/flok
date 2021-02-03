import os
from pathlib import Path


class Config:
    __slots__ = 'proxy_list', 'threads', 'path_driver', 'captcha_key'

    def __init__(self):
        with open("config/proxy.txt", 'r') as proxy_file:
            self.proxy_list = proxy_file

        self.threads = 6
        self.path_driver = '/drivers/chromedriver'
        self.captcha_key = '91588f4fb9475bde03fdfee20cd709ed'
