from selenium import webdriver


path_driver = './scripts/chromedriver'
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1480')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", prefs)
# TODO about proxy servers
# PROXY = "186.167.48.234:3128"
# chrome_options.add_argument('--proxy-server=%s' % PROXY)


# Read csv with inn, kpp, ogrn
# Validate on fire or after all loading
# Need to decide


# Simple alg
# - Get all collection pages with depth parameter
# - find
# - retrieve from coll



# Load set of links
# create bunch of threads  with links
# In one thread continue parse links
# This can help
# https://pastebin.com/QrZG9e9T
# https://pymotw.com/2/multiprocessing/basics.html
# https://medium.com/analytics-vidhya/asyncio-threading-and-multiprocessing-in-python-4f5ff6ca75e8