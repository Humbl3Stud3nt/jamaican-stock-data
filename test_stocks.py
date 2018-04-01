import unittest

from stocks import *

# TODO:
# Implement unit tests for all functions and classes

def test_get_trading_data():
    test_page = "stock_testing.html"
    with open(test_page) as f:
        test_html = f.read()
    test_soup = Soup(test_html, "lxml")
    rv = get_trading_data(test_soup)

    test_out = "test_out.csv"
    with open(test_out, "w") as f:
        print(rv, file=f)


if __name__ == "__main__":
    test_get_trading_data()
