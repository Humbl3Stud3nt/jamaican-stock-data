import unittest
import datetime
from bs4 import BeautifulSoup as Soup

from stocks import Instrument, get_soup, load_companies, update_companies

# TODO: Implement unit tests for all functions and classes
def create_instrument(num_trades):
    instr = Instrument()
    trade_days = [Instrument.TradeData(date=datetime.date.today() + datetime.timedelta(days=i)) for i in range(num_trades)]
    instr.trade_data = Instrument.TradeDataBanks(trade_days)

    return instr

@unittest.skip("Not implemented yet")
class StocksFunctionsTesting(unittest.TestCase):
    def test_get_soup(self):

        # TURN OFF INTERNET CONNECTION WHEN TESTING THIS
        with self.assertRaises(Exception):
            get_soup("https://www.jamstockex.com")

        self.assertTrue(isinstance(
            get_soup("http://www.jamstockex.com"), Soup))

    def test_gen_trade_data_url(self):
        pass

    def test_update_companies(self):
        pass

    def test_load_companies(self):
        pass

class TestGetRecordIndexByDate(unittest.TestCase):
    def setUp(self):
        self.instr = create_instrument(10)
        
    def test_get_record_index_by_date_get_last_record(self):
        self.assertEqual(self.instr.trade_data.get_record_index_by_date(datetime.date.today() + datetime.timedelta(days=9)), 9)
    
    def test_get_record_index_by_date_get_middle_record(self):
        self.assertEqual(self.instr.trade_data.get_record_index_by_date(datetime.date.today() + datetime.timedelta(days=5)), 5)

    def test_get_record_index_by_date_get_first_record(self):
        self.assertEqual(self.instr.trade_data.get_record_index_by_date(datetime.date.today()), 0)

    def test_get_record_index_by_date_get_crecord_out_of_range(self):
        self.assertIsNone(self.instr.trade_data.get_record_index_by_date(datetime.date.today() + datetime.timedelta(days=99)))
        

class TestInstrumentPlot(unittest.TestCase):
    def setUp(self):
        from TRADE_DATA import Instr_SVL
        self.instr = Instr_SVL.DATA
        # self.instr.update()
        # self.instr.store()

    def test_plot_with_valid_dates(self):
        start_date = datetime.date(2016, 8, 1)
        end_date = datetime.date(2016, 8, 30)
        try:
            self.instr.plot(start_date, end_date)
        except:
            self.fail("Error caught in test_plot_with_valid_dates()")

    def test_plot_with_start_date_and_no_end_date(self):
        start_date = datetime.date(2016, 8, 1)
        try:
            self.instr.plot(start_date)
        except:
            self.fail("Error caught in test_plot_with_start_date_and_no_end_date()")

    def test_plot_with_start_date_later_than_end_date(self):
        start_date = datetime.date(2016, 8, 1)
        end_date = datetime.date(2016, 7, 20)

        with self.assertRaises(ValueError):
            self.instr.plot(start_date, end_date)

    def test_plot_with_valid_start_date_and_end_date_out_of_range(self):
        start_date = datetime.date(2016, 8, 1)
        end_date = self.instr.get_trade_data().get_trade_days()[-1].get_date() + datetime.timedelta(days=1)

        with self.assertRaises(ValueError):
            self.instr.plot(start_date, end_date)

    def test_plot_with_start_date_out_of_range_and_valid_end_date(self):
        start_date = self.instr.get_trade_data().get_trade_days()[0].get_date() - datetime.timedelta(days=1)
        end_date = datetime.date(2016, 7, 20)

        with self.assertRaises(ValueError):
            self.instr.plot(start_date, end_date)


class TestInstrumentPlot_for(unittest.TestCase):
    def setUp(self):
        from TRADE_DATA import Instr_SVL
        self.instr = Instr_SVL.DATA
        # self.instr.update()
        # self.instr.store()

    def test_plot_for_with_date_in_range(self):
        num_days = len(self.instr.get_trade_data().get_trade_days())
        try:
            self.instr.plot_for(str(num_days)+"-d")
        except:
            self.fail("Error caught in test_plot_for_with_date_in_range()")

    def test_plot_for_with_date_out_of_range(self):
        num_days = 36500

        with self.assertRaises(ValueError):
            self.instr.plot_for(str(num_days)+"-d")

    

@unittest.skip("Not implemented yet")
class TestTradeDataClass(unittest.TestCase):
    pass

@unittest.skip("Not implemented yet")
class TestTradeDataBanksClass(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main(verbosity=5)
