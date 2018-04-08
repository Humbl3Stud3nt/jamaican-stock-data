import csv
import datetime
import os
import pprint
import json
import string
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as Soup

# TODO:
# MODIFY update_trade_data function to check last date updated and set url with that date as a starting date
# so that the number of rows to update is much lower than normal

# TODO:
# Implement store_data function, utilising .py files rather than .csv files

# TODO:
# Implement check to ensure that all pages checked have data to be access and skips them otherwise


# Constants
MAIN_MARKET_URL = "https://www.jamstockex.com/market-data/listed-companies/main-market"
JR_MARKET_URL = "https://www.jamstockex.com/market-data/listed-companies/junior-market"

MAIN_MARKET = "MAIN"
JR_MARKET = "JR"

TRADING_DATA_URL_BASE = "https://www.jamstockex.com/market-data/download-data/price-history/"

START_DATE = "1-01-01"

ILLEGAL_NUM_CHARS = list(string.punctuation)
ILLEGAL_NUM_CHARS.remove(".")

STOCK_INFO_DIR = "STOCK_INFO/"


class TradeDataBanks(object):
    """Class functioning as aggregate data-store for TradeData objects, makes up data-bank for each Instrument object"""

    def __init__(self, trade_days):
        assert type(trade_days) is list

        for value in trade_days:
            assert isinstance(value, TradeData)

        self.trades = trade_days

    def update(self, new_days):
        assert type(new_days) is list
        self.trades.extend(new_days)

    def load(self, file):
        pass

    def __str__(self):
        rv = ",".join(TradeData.HEADERS) + "\n"
        for day in self.get_trade_days():
            rv += str(day) + "\n"
        return rv

    def __repr__(self):
        return "TradeDataBanks(" + repr(self.trades) + ")"

    def get_most_recent(self):
        pass

    def get_trade_days(self):
        return self.trades


class TradeData(object):
    HEADERS = ("DATE", "CURRENT YEAR HIGH", "CURRENT YEAR LOW", "PREVIOUS YEAR DIVIDENDS",
               "CURRENT YEAR DIVIDENDS", "VOLUME", "TODAY'S HIGH", "TODAY'S LOW", "LAST TRADED PRICE", "CLOSING PRICE")

    def __init__(self, date=datetime.date(1, 1, 1), cur_yr_high=0, cur_yr_low=0, prev_yr_dvds=0.0, cur_yr_dvds=0.0, vol=0, today_high=0.0, today_low=0.0, last_traded_price=0.0, closing_price=0.0):
        assert isinstance(date, datetime.date)
        assert type(cur_yr_high) and type(cur_yr_low) and type(cur_yr_dvds) and type(prev_yr_dvds) and type(
            today_low) and type(today_high) and type(last_traded_price) and type(closing_price) is float
        assert type(vol) is int

        self.date = date
        self.cur_yr_high = cur_yr_high
        self.cur_yr_low = cur_yr_low
        self.prev_yr_dvds = prev_yr_dvds
        self.volume = vol
        self.cur_yr_dvds = cur_yr_dvds
        self.today_high = today_high
        self.today_low = today_low
        self.last_traded_price = last_traded_price
        self.closing_price = closing_price

    # Getter methods
    def get_date(self):
        return self.date
    def get_cur_yr_high(self):
        return self.cur_yr_high
    def get_cur_yr_low(self):
        return self.cur_yr_low
    def get_prev_dividends(self):
        return self.prev_yr_dvds
    def get_current_dividends(self):
        return self.cur_yr_dvds
    def get_today_high(self):
        return self.today_high
    def get_today_low(self):
        return self.today_low
    def get_last_traded_price(self):
        return self.last_traded_price
    def get_closing_price(self):
        return self.closing_price
    def get_volume(self):
        return self.volume

    def __repr__(self):
        return "TradeData(" + repr(self.date) + ", " + str(self.cur_yr_high) + ", " + str(self.cur_yr_low) + ", " + str(self.prev_yr_dvds) + ", " + str(self.cur_yr_dvds) + ", " + str(self.volume) + ", " + str(self.today_high) + ", " + str(self.today_low) + ", " + str(self.last_traded_price) + ", " + str(self.closing_price) + ")"
    
    def __str__(self):
        return str(self.date) + "," + str(self.cur_yr_high) + "," + str(self.cur_yr_low) + "," + str(self.prev_yr_dvds) + "," + str(self.cur_yr_dvds) + "," + str(self.volume) + "," + str(self.today_high) + "," + str(self.today_low) + "," + str(self.last_traded_price) + "," + str(self.closing_price)


class Instrument(object):
    def __init__(self, name="", stock_code="", currency="JMD", s_type="N/A", business_sector="N/A", trade_data=None):
        assert type(name) and type(stock_code) and type(
            currency) and type(s_type) and type(business_sector) is str
        # assert isinstance(trade_data, TradeData)
        try:
            assert "(SUSPENDED)" not in name
        except AssertionError:
            print("Stock: " + name + "not available")

        self.name = name
        self.code = stock_code
        self.currency = currency
        self.sector = business_sector
        self.s_type = s_type
        self.trade_data = trade_data

    # Getters

    def get_name(self):
        return self.name
    def get_code(self):
        return self.code
    def get_currency(self):
        return self.currency
    def get_sector(self):
        return self.sector
    def get_type(self):
        return self.s_type
    def get_trade_data(self):
        return self.trade_data

    def update_trade_data(self, trade_data):
        self.trade_data = trade_data

    def store_data(self):
        file = STOCK_INFO_DIR + self.get_name() + ".csv"
        with open(file, "w") as f:
            print(str(self.get_trade_data()), file=f)

    def __str__(self):
        return(self.get_name() + "," + self.get_code() + "," + self.get_currency() + "," + self.get_sector() + "," + self.get_type())

    def __repr__(self):
        return "Instrument(" + '"' + self.name + '"' + ", " + '"' + self.code + '"' + ", " + '"' + self.currency + '"' + ", " + '"' + self.s_type + '"' + ", " + '"' + self.sector + '"' + ", " + repr(self.trade_data) + ")"


def get_soup(url, retries=10):
    for i in range(retries):
        try:
            page = urlopen(url)
        except:
            if i < retries-1:
                continue
            else:
                raise Exception("Faulty internet connection. Could not access '" + url + "'" +
                                "\nTried " + str(retries) + " times")
        else:
            break

    page_html = page.read()
    page_soup = Soup(page_html, "lxml")
    page.close()
    return page_soup


def get_mkt_soup(url=MAIN_MARKET_URL):
    assert url == MAIN_MARKET_URL or url == JR_MARKET_URL
    return get_soup(url)


def get_company_data(mkt_soup):
    """Return list of Instrument objects detailing company data for all companies listed on the Jamaica stock exchange
    Accepts bs4.BeautifulSoup object as an argument
    Assumes that mkt_soup is a bs4.BeautifulSoup object referencing a page on the Jamaica stock exchange"""
    # Finds table of companies listed on the Jamaica stock exchange
    assert isinstance(mkt_soup, Soup)
    company_listing_table = mkt_soup.find("table")

    company_data = company_listing_table.findAll("tr")[1:]  # Excludes headers
    companies = []
    for row in company_data:
        row_company_info = row.findAll("td")
        name = row_company_info[0].text.strip()
        if "(SUSPENDED)" in name:
            continue
        code = row_company_info[1].text.strip()
        currency = row_company_info[2].text
        if len(row_company_info) == 6:
            sector = row_company_info[3].text
            share_type = row_company_info[4].text
        elif len(row_company_info) == 5:
            sector = "N/A"
            share_type = row_company_info[3].text

        companies.append(Instrument(name, code, currency,
                                    s_type=share_type, business_sector=sector))
    return companies


def gen_trade_data_url(instrument_code):
    current_date = datetime.date.today()
    return TRADING_DATA_URL_BASE + instrument_code + "/" + START_DATE + "/" + str(current_date)


def get_trading_soup(url):
    assert TRADING_DATA_URL_BASE in url
    return get_soup(url)


def get_trading_data(trading_soup):
    """Returns TradeDataBanks object containing data for each trade day of a particular Instrument
    """
    assert isinstance(trading_soup, Soup)

    def clean_num(num_string):
        """Helper function to get rid of whitespace and other illegal characters,
        making a formatted string of a number usable for calculations"""
        num_string = num_string.strip()

        for char in ILLEGAL_NUM_CHARS:
            if char in num_string:
                num_string = num_string.replace(char, "")

        return num_string

    trade_days = []
    table_body = trading_soup.find("table").find("tbody")
    table_rows = table_body.findAll("tr")

    for row in table_rows:
        columns = row.findAll("td")

        try:
            date = columns[1].text.strip()
        except:
            return None
        else:
            date = date.split("-")
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

            cur_yr_high = float(clean_num(columns[3].text))
            cur_yr_low = float(clean_num(columns[4].text))

            prev_yr_dvds = clean_num(columns[5].text)

            if prev_yr_dvds.isdecimal():
                prev_yr_dvds = float(prev_yr_dvds)
            else:
                prev_yr_dvds = 0.0

            cur_yr_dvds = clean_num(columns[6].text)

            if cur_yr_dvds.isdecimal():
                cur_yr_dvds = float(cur_yr_dvds)
            else:
                cur_yr_dvds = 0.0

            volume = int(clean_num(columns[7].text))

            today_high = float(clean_num(columns[8].text))
            today_low = float(clean_num(columns[9].text))
            last_traded_price = float(clean_num(columns[10].text))
            closing_price = float(clean_num(columns[11].text))

            trade_days.append(TradeData(date=date, cur_yr_high=cur_yr_high, cur_yr_low=cur_yr_low, prev_yr_dvds=prev_yr_dvds,
                                        cur_yr_dvds=cur_yr_dvds, vol=volume, today_high=today_high, today_low=today_low, last_traded_price=last_traded_price, closing_price=closing_price))
    return TradeDataBanks(trade_days)


def update_companies():
    file_path = "COMPANY_DATA.py"

    try:
        urlopen("https://www.jamstockex.com")
    except HTTPError:
        raise Exception("Could not update.")
    else:
        companies = []
        for company in get_company_data(get_mkt_soup(MAIN_MARKET_URL)):
            companies.append(company)
        for company in get_company_data(get_mkt_soup(JR_MARKET_URL)):
            companies.append(company)
        with open(file_path, "w") as fp:
            print("###############################", file=fp)
            print("# DO NOT EDIT THIS FILE!!!!!!!#", file=fp)
            print("###############################", file=fp)
            print("from stocks import Instrument, TradeData, TradeDataBanks\n", file=fp)
            print("ALL_DATA = " + pprint.pformat(companies, indent=4), file=fp) 
        print("Successfully updated.")


def load_companies():
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

# FIXME: create a generator that allows incremental writing of the list object to a .py file for later reference
def store_data():
    company_trade_data = []
    file_path = "COMPANY_TRADE_DATA.py"

    for company in load_companies():
        company.update_trade_data(get_trading_data(
            get_trading_soup(gen_trade_data_url(company.get_code()))))
        company_trade_data.append(company)
        with open(file_path, "w") as fp:
            fp.write("###############################\n# DO NOT EDIT THIS FILE!!!!!!!#\n###############################\n")
            fp.write("import datetime\n")
            fp.write("from stocks import Instrument, TradeData, TradeDataBanks\n")
            print("ALL_DATA = " + pprint.pformat(company_trade_data), file=fp) 
        print("Successfully stored: " + company.get_name() + " data")
        # break


def main():
    update_companies()
    store_data()


if __name__ == "__main__":
    main()

