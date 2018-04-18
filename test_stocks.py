import unittest

from stocks import *

# TODO:
# Implement unit tests for all functions and classes

class StocksFunctionsTesting(unittest.TestCase):
    def test_get_soup(self):

        # TURN OFF INTERNET CONNECTION WHEN TESTING THIS
        with self.assertRaises(Exception):
            get_soup("http://www.youtube.com")
        
        self.assertTrue(isinstance(get_soup("http://www.jamstockex.com"), Soup))

    def test_gen_trade_data_url(self):
        pass
    
    def test_update_companies(self):
        pass

    def test_load_companies(self):
        pass

    
class StocksInstrumentTesting(unittest.TestCase):
    pass

class StocksTradeDataTesting(unittest.TestCase):
    pass

class StocksTradeDataBanksTesting(unittest.TestCase):
    pass





if __name__ == "__main__":
    unittest.main()
