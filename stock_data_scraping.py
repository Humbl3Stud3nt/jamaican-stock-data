import datetime
import pprint
import string
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as Soup

import utils

# URL Constants
MAIN_MARKET_URL = "https://www.jamstockex.com/market-data/listed-companies/main-market"
JR_MARKET_URL = "https://www.jamstockex.com/market-data/listed-companies/junior-market"


#@utils.timing
def get_soup(url, retries=10):
    """
    Return bs4.BeautifulSoup object representation of the page whose url is passed as 'url'

    Retries connection until successful up to 'retries' times 
    If unsuccesful, raise an Exception 
    """
    for i in range(retries):
        try:
            page = urlopen(url)
        except:
            if i < retries-1:
                continue
            else:
                raise Exception("Faulty internet connection. Could not access '%s'" % url +
                                "\nTried %d times." % retries)
        else:
            break

    page_html = page.read()
    page_soup = Soup(page_html, "lxml")
    page.close()
    return page_soup
