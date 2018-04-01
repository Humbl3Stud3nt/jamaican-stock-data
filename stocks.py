import csv
import datetime
import json
import os
import string
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as Soup

# Constants
MAIN_MARKET_URL = "https://www.jamstockex.com/market-data/listed-companies/main-market"
JR_MARKET_URL = "https://www.jamstockex.com/market-data/listed-companies/junior-market"

MAIN_MARKET = "MAIN"
JR_MARKET = "JR"

TRADING_DATA_URL_BASE = "https://www.jamstockex.com/market-data/download-data/price-history/"

START_DATE = "1-01-01"

ILLEGAL_NUM_CHARS = list(string.punctuation)
ILLEGAL_NUM_CHARS.remove(".")

STOCK_INFO_DIR = "STOCK_INFO\\"


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

    def get_most_recent(self):
        pass

    def get_trade_days(self):
        return self.trades


class TradeData(object):
    HEADERS = ("DATE", "CURRENT YEAR HIGH", "CURRENT YEAR LOW", "PREVIOUS YEAR DIVIDENDS",
               "CURRENT YEAR DIVIDENDS", "VOLUME", "TODAY'S HIGH", "TODAY'S LOW", "LAST TRADED PRICE", "CLOSING PRICE")

    def __init__(self, date, cur_yr_high, cur_yr_low, prev_yr_dvds, cur_yr_dvds, vol, today_high, today_low, last_traded_price, closing_price):
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

    def get_current_dividents(self):
        return self.cur_yr_dvds

    def get_today_high(self):
        return self.today_high

    def get_today_low(self):
        return self.today_low

    def get_last_traded_price(self):
        return self.last_traded_price

    def get_closing_price(self):
        return self.closing_price

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


def get_soup(url, retries = 10):
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


def clean_num(num_string):
    num_string = num_string.strip()

    for char in ILLEGAL_NUM_CHARS:
        if char in num_string:
            num_string = num_string.replace(char, "")

    return num_string


def get_trading_data(trading_soup):
    """Returns TradeDataBanks object containing data for each trade day of a particular Instrument
    """
    assert isinstance(trading_soup, Soup)
    trade_days = []

    table_body = trading_soup.find("table").find("tbody")

    table_rows = table_body.findAll("tr")

    for row in table_rows:
        columns = row.findAll("td")

        date = columns[1].text.strip()
        date = date.split("-")

        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

        cur_yr_high = float(clean_num(columns[3].text))
        cur_yr_low = float(clean_num(columns[4].text))

        prev_yr_dvds = clean_num(columns[5].text)

        if prev_yr_dvds.isdecimal():
            prev_yr_dvds = float(prev_yr_dvds)

        cur_yr_dvds = clean_num(columns[6].text)

        if cur_yr_dvds.isdecimal():
            cur_yr_dvds = float(cur_yr_dvds)

        volume = int(clean_num(columns[7].text))

        today_high = float(clean_num(columns[8].text))
        today_low = float(clean_num(columns[9].text))
        last_traded_price = float(clean_num(columns[10].text))
        closing_price = float(clean_num(columns[11].text))

        trade_days.append(TradeData(date, cur_yr_high, cur_yr_low, prev_yr_dvds,
                                    cur_yr_dvds, volume, today_high, today_low, last_traded_price, closing_price))
    return TradeDataBanks(trade_days)


def update_companies():
    file_path = "COMPANY DATA.csv"

    try:
        urlopen("https://www.jamstockex.com")
    # except URLError:
    #     raise Exception("Faulty internet connection. Could not update.")
    except HTTPError:
        raise Exception("Fatal Error. Page not found")
    else:
        with open(file_path, "w") as fp:
            fp.write("INSTRUMENT NAME,INSTRUMENT CODE,CURRENCY,SECTOR,SHARE TYPE\n")
            for company in get_company_data(get_mkt_soup(MAIN_MARKET_URL)):
                fp.write(str(company) + "\n")
            for company in get_company_data(get_mkt_soup(JR_MARKET_URL)):
                fp.write(str(company) + "\n")
        print("Successfully updated.")


def load_companies(file="COMPANY DATA.csv"):
    companies = []
    with open(file) as f:
        rows = csv.reader(f.readlines())

    row_data = []
    for row in rows:
        row_data.append(row)

    for i in range(1, len(row_data)):
        companies.append(Instrument(
            name=row_data[i][0], stock_code=row_data[i][1], currency=row_data[i][2], business_sector=row_data[i][3], s_type=row_data[i][4]))
        yield companies[-1]


def main():
    # update_companies()
    for company in load_companies():
        company.update_trade_data(get_trading_data(
            get_trading_soup(gen_trade_data_url(company.get_code()))))
        company.store_data()
        print("Successfully stored: " + company.get_name() + " data")

if __name__ == "__main__":
    main()
