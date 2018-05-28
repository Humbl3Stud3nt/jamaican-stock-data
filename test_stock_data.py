import unittest
import datetime
from bs4 import BeautifulSoup as Soup

from stock_data import Instrument, get_soup, load_companies, update_companies

# TODO: Implement unit tests for all functions and classes
def create_instrument(num_trades):
    instr = Instrument()
    trade_days = [Instrument.TradeData(date=datetime.date.today() + datetime.timedelta(days=i)) for i in range(num_trades)]
    instr.trade_data = Instrument.TradeDataBanks(trade_days)

    return instr

class TestGetSoup(unittest.TestCase):
    def test_get_soup_with_valid_url(self):
        self.assertTrue("http://www.jamstockex.com", Soup)

    def test_get_soup_with_invalid_url(self):
        with self.assertRaises(Exception):
            get_soup("http://www.jamstockexcom")
    
    @unittest.skip("Not implemented yet")
    def test_get_soup_with_bad_connection(self):
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
        

class TestInstrument__Plot(unittest.TestCase):
    def setUp(self):
        from TRADE_DATA import Instr_SVL
        self.instr = Instr_SVL.DATA


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


class TestInstrument__Plot_for(unittest.TestCase):
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

    
class TestTradeData__equal__(unittest.TestCase):
    def test__eq__with_identical_TradeData_objects(self):
        a = Instrument.TradeData(date=datetime.date(2012, 1, 1))
        b = Instrument.TradeData(date=datetime.date(2012, 1, 1))
        print(a)
        print(b)
        self.assertTrue(a == b)

    def test__eq__with_TradeData_objects_with_different_dates(self):
        a = Instrument.TradeData(date=datetime.date(2012, 1, 1))
        b = Instrument.TradeData(date=datetime.date(2012, 1, 2))
        print(a)
        print(b)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_cur_yr_high(self):
        a = Instrument.TradeData(cur_yr_high=1)
        b = Instrument.TradeData(cur_yr_high=2)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_cur_yr_low(self):
        a = Instrument.TradeData(cur_yr_low=1)
        b = Instrument.TradeData(cur_yr_low=2)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_prev_dividends(self):
        a = Instrument.TradeData(prev_yr_dvds=1)
        b = Instrument.TradeData(prev_yr_dvds=2)
        self.assertFalse(a == b)
    
    def test__eq__with_TradeData_objects_with_different_cur_dividends(self):
        a = Instrument.TradeData(cur_yr_dvds=1)
        b = Instrument.TradeData(cur_yr_dvds=2)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_today_high(self):
        a = Instrument.TradeData(today_high=1)
        b = Instrument.TradeData(today_high=2)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_today_low(self):
        a = Instrument.TradeData(today_low=1)
        b = Instrument.TradeData(today_low=2)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_last_traded_price(self):
        a = Instrument.TradeData(last_traded_price=1)
        b = Instrument.TradeData(last_traded_price=2)
        self.assertFalse(a == b)

    def test__eq__with_TradeData_objects_with_different_closing_price(self):
        a = Instrument.TradeData(closing_price=1)
        b = Instrument.TradeData(closing_price=2)
        self.assertFalse(a == b)
    
    def test__eq__with_TradeData_objects_with_different_volume_traded(self):
        a = Instrument.TradeData(vol=1)
        b = Instrument.TradeData(vol=2)
        self.assertFalse(a == b)


@unittest.skip("Not implemented yet")
class TestTradeDataBanks__sort(unittest.TestCase):
    def setUp(self):
        day_list = [Instrument.TradeData(date=datetime.date(2012, 1, i)) for i in range(1, 30)]
        self.dataBanks = Instrument.TradeDataBanks(day_list)
    
    def test__sort__(self):
        pass

@unittest.skip("Not implemented yet")
class TestTradeDataBanks__add__(unittest.TestCase):
    pass

@unittest.skip("Not implemented yet")
class TestTradeDataBanks__get_record_index_by_date(unittest.TestCase):
    pass

@unittest.skip("Not implemented yet")
class TestTradeDataBanks__get_record_by_date(unittest.TestCase):
    pass


def main():
    unittest.main(module="test_stock_data", verbosity=5)

if __name__ == "__main__":
    main()
