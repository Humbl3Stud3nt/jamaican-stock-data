import datetime
import pprint
import string
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as Soup

import utils
from stock_data import Instrument

ILLEGAL_NUM_CHARS = ('!', '"', '#', '$', '%',
                     '&', "'", '(', ')', '*',
                     '+', ',', '-', '/', ':',
                     ';', '<', '=', '>', '?',
                     '@', '[', '\\', ']', '^',
                     '_', '`', '{', '|', '}', '~')
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

#@utils.timing
def get_company_data(mkt_soup):
    """
    Return list of Instrument objects detailing company data for all companies listed on the Jamaica stock exchange
    Accepts bs4.BeautifulSoup object as an argument
    Assumes that mkt_soup is a bs4.BeautifulSoup object referencing a page on the Jamaica stock exchange
    """
    # Finds table of companies listed on the Jamaica stock exchange
    assert isinstance(mkt_soup, Soup)
    company_listing_table = mkt_soup.find("table")

    rows = company_listing_table.findAll("tr")[1:]  # Excludes headers
    companies = []
    for row in rows:
        company_info = row.findAll("td")
        name = company_info[0].text.strip()
        if "(SUSPENDED)" in name:  # Skip this instrument and move to the next
            continue
        code = company_info[1].text.strip()
        currency = company_info[2].text

        # If the sector is given, use store that text and use column 5 as the share type
        if len(company_info) == 6:
            sector = company_info[3].text
            share_type = company_info[4].text
        # If sector is not given, set sector as "N/A" and use column 4 as the share type
        elif len(company_info) == 5:
            sector = "N/A"
            share_type = company_info[3].text

        companies.append(Instrument(name, code, currency,
                                    s_type=share_type, business_sector=sector))
    return companies


#@utils.timing
def get_trading_data(trading_soup):
    """
    Return Instrument.TradeDataBanks object containing data for each trade day of a particular Instrument
    """
    assert isinstance(trading_soup, Soup)

    def _clean_num(num_string):
        """
        Return a formatted string of a number to be converted to float or int
        """
        num_string = num_string.strip()
        for char in ILLEGAL_NUM_CHARS:
            if char in num_string:
                num_string = num_string.replace(char, "")
        return num_string

    trade_days = []
    table_rows = trading_soup.find("table").find("tbody").findAll("tr")

    for row in table_rows:
        # Create Instrument.TradeData object for each row of data
        columns = row.findAll("td")
        # TODO: Make this fail more loudly

        # Check if on the right page, if not, return None
        try:
            date_text = columns[1].text.strip()
        except:
            return None
        else:
            # Extract date
            date_values = date_text.split("-")
            date = datetime.date(int(date_values[0]), int(
                date_values[1]), int(date_values[2]))

            # Extract current year high and current year low
            cur_yr_high, cur_yr_low = float(_clean_num(
                columns[3].text)), float(_clean_num(columns[4].text))

            # Extract previous year dividends
            prev_yr_dvds = _clean_num(columns[5].text)
            if prev_yr_dvds.isdecimal():
                prev_yr_dvds = float(prev_yr_dvds)
            else:
                prev_yr_dvds = 0.0

            # Extract current year dividends
            cur_yr_dvds = _clean_num(columns[6].text)
            if cur_yr_dvds.isdecimal():
                cur_yr_dvds = float(cur_yr_dvds)
            else:
                cur_yr_dvds = 0.0

            volume = int(_clean_num(columns[7].text))
            today_high = float(_clean_num(columns[8].text))
            today_low = float(_clean_num(columns[9].text))
            last_traded_price = float(_clean_num(columns[10].text))
            closing_price = float(_clean_num(columns[11].text))

            trade_days.append(Instrument.TradeData(date=date, cur_yr_high=cur_yr_high, cur_yr_low=cur_yr_low, prev_yr_dvds=prev_yr_dvds,
                                                   cur_yr_dvds=cur_yr_dvds, vol=volume, today_high=today_high, today_low=today_low, last_traded_price=last_traded_price, closing_price=closing_price))
    return Instrument.TradeDataBanks(trade_days)


#@utils.timing
def update(self):
    """
    Check http://www.jamstockex.com for new data
    Update trade_data and change self.last_updated value to the current utc timestamp
    """
    trade_data_url = self.gen_trade_data_url()
    self.update_trade_data(get_trading_data(get_soup(trade_data_url)))
    self.last_updated = datetime.datetime.timestamp(
        datetime.datetime.utcnow())

def update_companies():
    """
    Update COMPANY_DATA.py file with Instrument objects for all companies on the JSE
    """
    print("Attempting to update...")
    file_path = "COMPANY_DATA.py"

    try:
        urlopen("https://www.jamstockex.com")
    except HTTPError:
        raise Exception("Could not update.")
    except URLError:
        raise Exception("Could not update.")
    else:
        print("Updating list of companies...")
        companies = []
        for company in get_company_data(get_soup(MAIN_MARKET_URL)):
            companies.append(company)
        for company in get_company_data(get_soup(JR_MARKET_URL)):
            companies.append(company)
        with open(file_path, "w") as fp:
            fp.write("###############################\n")
            fp.write("# DO NOT EDIT THIS FILE!!!!!!!#\n")
            fp.write("###############################\n")
            fp.write("import datetime\n")
            fp.write("from stock_data import Instrument\n")
            fp.write("ALL_DATA = " + pprint.pformat(companies, indent=4))
        print("Successfully updated.")


def load_companies():
    """
    Create generator object listing companies in COMPANY_DATA.ALL_DATA"""
    try:
        from COMPANY_DATA import ALL_DATA
    except:
        print("Data not found.\nAttempting to populate file...")
        update_companies()
        from COMPANY_DATA import ALL_DATA
    finally:
        companies = ALL_DATA
        for company in companies:
            yield company


def store_data():
    """
    Write all trade_data to a file for each instrument.
    """
    for company in load_companies():
        company.update()
        company.store()
        print("Successfully stored: " + company.get_name() + " data.\n")


def update_and_store():
    """
    Update trade data for all instruments
    """
    update_companies()
    store_data()


def full_update():
    update_companies()
    update_and_store()
