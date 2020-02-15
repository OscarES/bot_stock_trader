import os
import quandl
import datetime
import csv
from pathlib import Path
 
quandl.ApiConfig.api_key = 'nYSMyLz8EGPfU8sVwjxd'


def quandl_stocks(symbol, start_date=(2000, 1, 1), end_date=None):
    """
    symbol is a string representing a stock symbol, e.g. 'AAPL'

    start_date and end_date are tuples of integers representing the year, month,
    and day

    end_date defaults to the current date when None
    """

    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]

    start_date = datetime.date(*start_date)

    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()

    return quandl.get(query_list, 
                      returns='pandas', 
                      start_date=start_date,
                      end_date=end_date,
                      collapse='daily',
                      order='asc')


if __name__ == '__main__':
    bad_tickers_file = 'bad_tickers.txt'
    number_of_calls = 0  # (1)
    with open('/mnt/c/Users/oscar/Documents/Stocks/quandl/EOD_metadata.csv') as ticker_database:
        reader = csv.reader(ticker_database)
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            ticker = row[0]
            print('')
            print(ticker)
            # print(row[2])  # shows the description column
            # skip bad tickers
            if ticker == 'AA_P':
                continue
            with open(bad_tickers_file) as bad_tickers:
                if '\n' + ticker + '\n' in bad_tickers.read():
                    print('Skipping bad ticker: ' + ticker)
                    continue

            ticker_file = Path('/mnt/c/Users/oscar/Documents/Stocks/automatic_quandl/' \
                               + ticker + '.csv')
            empty_file_size = 2000  # (bytes)
            if not ticker_file.is_file() or os.stat(ticker_file).st_size < empty_file_size:
                from_date = row[4]
                to_date = row[5]
                # print(from_date)
                # print(to_date)
                try:
                    ticker_data = quandl_stocks(ticker,
                                                start_date=(int(from_date[0:4]),
                                                            int(from_date[5:7]),
                                                            int(from_date[8:])),
                                                end_date=(int(to_date[0:4]),
                                                          int(to_date[5:7]),
                                                          int(to_date[8:])))
                    ticker_data.to_csv(ticker_file, encoding='utf-8')
                    print('Succesfully downloaded: ' + ticker)
                except ValueError:
                    with open(bad_tickers_file, 'a') as bad_tickers:
                        bad_tickers.write(ticker + '\n')
                    print('Could not download: ' + ticker)
            else:
                print('Already downloaded: ' + ticker)

