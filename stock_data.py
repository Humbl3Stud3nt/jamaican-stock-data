"""
author: Warren James
Program name: Stocks manager

Purpose: This program is intended to make records of the Jamaica stock exchange to create a local database of stock
data which can be used to make decisions about stock trading.

Features:
    - Visual representation of stock data over time
    - Comparison of stock data over time
    - Local generation and storage of records of stocks on the stock exchange
    - More coming soon
    
"""
import datetime
import os
import pprint
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pylab
from bs4 import BeautifulSoup as Soup

import stock_data_scraping as scr
import utils

# TODO:
# Implement data representation methods for stock Instruments
# CONSTANTS
ILLEGAL_NUM_CHARS = ('!', '"', '#', '$', '%',
                     '&', "'", '(', ')', '*',
                     '+', ',', '-', '/', ':',
                     ';', '<', '=', '>', '?',
                     '@', '[', '\\', ']', '^',
                     '_', '`', '{', '|', '}', '~')
TRADING_DATA_URL_BASE = "https://www.jamstockex.com/market-data/download-data/price-history/"

# Debugging flag
DEBUG = False

class Instrument(object):
    """
    Object representing a particular instrument on the Jamaica stock exchange.
    """

    def __init__(self, name="", stock_code="", currency="JMD", s_type="N/A", business_sector="N/A", trade_data=None, last_updated=None):
        assert type(name) and type(stock_code) and type(
            currency) and type(s_type) and type(business_sector) is str
        try:
            assert "(SUSPENDED)" not in name
        except AssertionError:
            print("Stock: " + name + " not available")

        self.name = name
        self.code = stock_code
        self.currency = currency
        self.sector = business_sector
        self.s_type = s_type
        self.trade_data = trade_data

        if last_updated is None:
            self.last_updated = 0.0
        else:
            self.last_updated = last_updated

        # Creates file name for data storage
        self.file_path = "Instr_" + self.code.replace(".", "_") + ".py"

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
        self.trade_data = Instrument.TradeDataBanks.__add__(
            self.trade_data, trade_data)

    def update(self):
        """
        Check http://www.jamstockex.com for new data
        Update trade_data and change self.last_updated value to the current utc timestamp
        """
        trade_data_url = self.gen_trade_data_url()
        self.update_trade_data(get_trading_data(scr.get_soup(trade_data_url)))
        self.last_updated = datetime.datetime.timestamp(
            datetime.datetime.utcnow())

    def get_figure_for_past(self, period="3-m", option="closing price"):
        """
        Plot for a period of time up to the current date
        """
        num_days = _parse_period(period)
        end_date = self.trade_data.get_trade_days()[-1].get_date()
        start_date = end_date - datetime.timedelta(num_days)
        return self.get_figure(start_date, end_date, option)

    def get_figure(self, start_date, end_date=None, option="closing price"):
        """
        Return tuples of dates and values of selected metrics
        (specified by 'option'), from 'start-date' to 'end_date'
        """
        def _get_func(option):
            OPTION_TABLE = {"closing price":(Instrument.TradeData.get_closing_price, "Closing Price (JMD)"),
                            "cur_year_dvds":(Instrument.TradeData.get_current_dividends, "Current Year Dividends (JMD)"),
                            "prev_year_dvds": (Instrument.TradeData.get_prev_dividends, "Previous Year Dividends (JMD)"),
                            "day_high":(Instrument.TradeData.get_today_high, "Today's High (JMD)"),
                            "day_low": (Instrument.TradeData.get_today_low, "Today's Low (JMD)"),
                            "volume": (Instrument.TradeData.get_volume, "Volume Traded")
                            }
            try:
                return OPTION_TABLE[option]
            except KeyError:
                print("'" + option + "'" + " is not a valid option.\nValid options are: \n" + "\n".join(tuple(OPTION_TABLE.keys())))
                raise Exception
            

        def _get_fig(getter_func, y_label, start_date=start_date, end_date=end_date):
            trade_data = self.get_trade_data()
            earliest_record = trade_data.get_trade_days()[0].get_date()
            latest_record = trade_data.get_trade_days()[-1].get_date()

            if start_date >= earliest_record:
                if end_date is None:
                    end_date = latest_record
                elif end_date > latest_record:
                    raise ValueError("No data for " + str(end_date))
                else:
                    try:
                        assert start_date < end_date
                    except AssertionError:
                        raise ValueError("Start date cannot come before end date.")
                    while True:
                        try:
                            index = trade_data.get_record_index_by_date(start_date)
                            assert type(index) is int
                        except AssertionError:
                            start_date += datetime.timedelta(days=1)
                        else:
                            break

                    records = []
                    date = start_date
                    
                    while date < end_date:
                        new_record = trade_data.get_trade_days()[index]
                        records.append(new_record)
                        date = new_record.get_date()
                        index += 1

                    dates = tuple([record.get_date() for record in records])
                    data = tuple([getter_func(record) for record in records])

                    figure = pylab.matplotlib.figure.Figure(figsize=(5,4), dpi=100)
                    subplot = figure.add_subplot(111, xlabel="Date", ylabel=y_label, title="{} {} for past ... ".format(self.name, y_label))
                    subplot.grid()
                    subplot.plot(dates, data)
                    # figure.add_subplot(subplot)
                    # figure.add_subplot(111).xlabel("Date")
                    # figure.add_subplot(111).ylabel(y_label)
                    # figure.add_subplot(111).xticks(rotation=-55)
                    # figure.add_subplot(111).grid()

                    return figure

            else:
                raise ValueError("No data for " + str(start_date))

        return _get_fig(*_get_func(option))

    #@utils.timing
    def store(self):
        file_path = "TRADE_DATA" + os.path.sep + self.file_path
        with open(file_path, "w") as fp:
            fp.write("###############################\n")
            fp.write("# DO NOT EDIT THIS FILE!!!!!!!#\n")
            fp.write("###############################\n")
            fp.write("import datetime\n")
            fp.write("from stock_data import Instrument\n")
            fp.write("DATA" + " = " + pprint.pformat(self, indent=4))

    def gen_trade_data_url(self):
        """
        Return appropriate url to access new stock data on http://www.jamstockex.com
        """
        start_date = datetime.date.fromtimestamp(self.last_updated)
        end_date = datetime.date.today()

        return TRADING_DATA_URL_BASE + self.get_code() + "/" + str(start_date) + "/" + str(end_date)

    def __str__(self):
        return self.get_name() + "," + self.get_code() + "," + self.get_currency() + "," + self.get_sector() + "," + self.get_type()

    def __repr__(self):
        return "Instrument(" + '"' + self.name + '"' + ", " + '"' + self.code + '"' + ", " + '"' + self.currency + '"' + ", " + '"' + self.s_type + '"' + ", " + '"' + self.sector + '"' + ", " + repr(self.trade_data) + ", " + "last_updated=" + str(self.last_updated) + ")"

    class TradeDataBanks(object):
        """
        Sorted list-like container for Instrument.TradeData objects
        """

        def __init__(self, trade_days):
            assert type(trade_days) is list

            for value in trade_days:
                assert isinstance(value, Instrument.TradeData)

            self.trades = trade_days
            self.sort()

        def update(self, new_days):
            assert type(new_days) is list
            self.trades.extend(new_days)

        def sort(self):
            """
            Sorts trades from oldest to newest
            """
            sort_func = lambda x: Instrument.TradeData.get_date(x)
            self.trades = sorted(self.trades, key=sort_func)

        def __add__(self, other):
            """
            Implement '+' with 
            <Instrument.TradeDataBanks1> + <Instrument.TradeDataBanks2> 
            syntax where the result is another Instrument.TradeDataBanks object with any duplicates removed
            """

            def _update_list(list1, list2):
                """
                Return the union of list1 and list2
                """
                if list1 == list2:
                    return list1
                elif len(list1) > len(list2):
                    short_list, long_list = list2, list1
                else:
                    short_list, long_list = list1, list2
                new_list = []
                for i in range(len(short_list)):
                    if short_list[i] not in long_list:
                        new_list.append(short_list[i])
                return long_list + new_list

            if isinstance(other, Instrument.TradeDataBanks) and isinstance(self, Instrument.TradeDataBanks):
                rv = Instrument.TradeDataBanks(
                    _update_list(self.trades, other.trades))

                return rv

            elif other is None and isinstance(self, Instrument.TradeDataBanks):
                return self
            elif self is None and isinstance(other, Instrument.TradeDataBanks):
                return other
            elif self is None and other is None:
                return None
            else:
                raise ValueError

        def __len__(self):
            return len(self.trades)

        def __str__(self):
            rv = ",".join(Instrument.TradeData.HEADERS) + "\n"
            for day in self.get_trade_days():
                rv += str(day) + "\n"
            return rv

        def __repr__(self):
            return "Instrument.TradeDataBanks(" + repr(self.trades) + ")"

        def get_trade_days(self):
            return self.trades.copy()

        def get_record_index_by_date(self, date):
            """
            Return index of Instrument.TradeData object with date attribute given as an argument if it exists
            Otherwise return None
            """
            trade_days = self.get_trade_days()
            dates = [record.get_date() for record in trade_days]

            try:
                return dates.index(date)
            except ValueError:
                return None

        def get_record_by_date(self, date):
            """
            Return Instrument.TradeData object with date attribute given as argument if it exists
            Otherwise, return None
            """
            record_index = self.get_record_index_by_date(date)
            if record_index is None:
                return None
            else:
                return self.trades[record_index]

    class TradeData(object):
        """
        Class representing a record for a single market day
        """
        HEADERS = ("DATE", "CURRENT YEAR HIGH", "CURRENT YEAR LOW", "PREVIOUS YEAR DIVIDENDS",
                   "CURRENT YEAR DIVIDENDS", "VOLUME", "TODAY'S HIGH", "TODAY'S LOW", "LAST TRADED PRICE", "CLOSING PRICE")

        def __init__(self, date=datetime.date(1, 1, 1), cur_yr_high=0, cur_yr_low=0, prev_yr_dvds=0.0, cur_yr_dvds=0.0, vol=0, today_high=0.0, today_low=0.0, last_traded_price=0.0, closing_price=0.0):
            assert isinstance(date, datetime.date)
            assert(
                type(cur_yr_high) and 
                type(cur_yr_low) and 
                type(cur_yr_dvds) and 
                type(prev_yr_dvds) and 
                type(today_low) and 
                type(today_high) and 
                type(last_traded_price) and 
                type(closing_price) is float or int
            )

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

        def __eq__(self, other):
            if self.date == other.date and self.cur_yr_high == other.cur_yr_high and self.cur_yr_low == other.cur_yr_low and self.cur_yr_dvds == other.cur_yr_dvds and self.prev_yr_dvds == other.prev_yr_dvds and self.volume == other.volume and self.today_high == other.today_low and self.last_traded_price == other.last_traded_price and self.closing_price == other.closing_price:
                return True
            else:
                return False

        def __repr__(self):
            return "Instrument.TradeData(" + repr(self.date) + ", " + str(self.cur_yr_high) + ", " + str(self.cur_yr_low) + ", " + str(self.prev_yr_dvds) + ", " + str(self.cur_yr_dvds) + ", " + str(self.volume) + ", " + str(self.today_high) + ", " + str(self.today_low) + ", " + str(self.last_traded_price) + ", " + str(self.closing_price) + ")"

        def __str__(self):
            return str(self.date) + "," + str(self.cur_yr_high) + "," + str(self.cur_yr_low) + "," + str(self.prev_yr_dvds) + "," + str(self.cur_yr_dvds) + "," + str(self.volume) + "," + str(self.today_high) + "," + str(self.today_low) + "," + str(self.last_traded_price) + "," + str(self.closing_price)

def _parse_period(period_code):
            UNITS = {"d": 1,"w": 7, "m": 30, "y": 366}
            assert type(period_code) is str
            mult, unit = tuple(period_code.split("-"))
            try:
                assert mult.isdigit()
                assert unit in UNITS
            except:
                print("Invalid period code: " + period_code + " given as argument.")

            num_days = int(mult)*UNITS[unit]
            return num_days

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
        for company in get_company_data(scr.get_soup(scr.MAIN_MARKET_URL)):
            companies.append(company)
        for company in get_company_data(scr.get_soup(scr.JR_MARKET_URL)):
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


if __name__ == "__main__":
    if DEBUG:  # Run unit tests
        import test_stock_data
        test_stock_data.main()
    else:
        while True:
            choice = input("You are about to update the entire database. Are you sure you wan to do this? (Y/N)\n\n")
            print("\n")
            if choice.lower() == "y":
                update_and_store()
                break
            elif choice.lower() == "n":
                print("Exiting")
                break
            else:
                print("Invalid option.\n\n")
