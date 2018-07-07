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

import pylab

import utils

# TODO:
# Implement data representation methods for stock Instruments
# CONSTANTS
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



    def plot_for(self, period="3-m", option="closing price"):
        """"
        Plot for a period of time up to the current date
        """
        num_days = _parse_period(period)
        end_date = self.trade_data.get_trade_days()[-1].get_date()
        start_date = end_date - datetime.timedelta(num_days)
        self.plot(start_date, end_date, option)

    def plot(self, start_date, end_date=None, option="closing price"):
        """
        Create a graph showing the value of selected metrics over a certain period of time,
        specified by 'start_date' and 'end_date' and 'option'
        """
        def _get_func(option):
            OPTION_TABLE = {"closing price":Instrument.TradeData.get_closing_price,
                            "cur_year_dvds":Instrument.TradeData.get_current_dividends,
                            "prev_year_dvds": Instrument.TradeData.get_prev_dividends,
                            "day_high":Instrument.TradeData.get_today_high,
                            "day_low": Instrument.TradeData.get_today_low,
                            "volume": Instrument.TradeData.get_volume
                            }
            try:
                return OPTION_TABLE[option]
            except KeyError:
                print("'" + option + "'" + " is not a valid option.\nValid options are: \n" + "\n".join(tuple(OPTION_TABLE.keys())))
                raise Exception
            

        def _gen_graph(getter_func, start_date=start_date, end_date=end_date):
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

                    dates = [record.get_date() for record in records]
                    data = [getter_func(record) for record in records]

                    pylab.figure(self.get_name() + " " + option)
                    pylab.title(self.get_name() + " " + option + " against Time")
                    pylab.xlabel("Date")
                    pylab.ylabel(option)
                    pylab.xticks(rotation=-55)
                    pylab.grid()
                    pylab.plot(dates, data)
                    pylab.show()

            else:
                raise ValueError("No data for " + str(start_date))

        _gen_graph(_get_func(option))

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

if __name__ == "__main__":
    if DEBUG:  # Run unit tests
        import test_stock_data
        test_stock_data.main()
    else:
        from stock_data_scraping import update_and_store
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
