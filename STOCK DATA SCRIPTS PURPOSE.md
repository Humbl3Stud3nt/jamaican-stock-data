# Stock data scripts

## Purpose

Parse most recent stock data for all instruments on Jamaica stock exchange
Store data for each day the stocks are updated in an expanding spreadsheet

## Dependencies

- csv *(?)*
- beautifulsoup4
- urllib
- selenium(possibly)
- openpyxl
- datetime
- os

## Tasks

- generate site url
  - need stock name
  - need url base for jamaica stock exchange website
- parse site for most recent stock data
- store stock data as an object
- write stock data to a spreadsheet*
  - use one workbook, but make a copy of it, and in the case of the throwing of an exception that would cause corruption of data, store that copy, else delete it
