import quandl
import datetime
 
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
    # apple_data = quandl_stocks('AAPL', start_date=(2000, 1, 1), end_date=(2000, 1, 3))
    apple_data = quandl_stocks('AAPL', start_date=(2000, 1, 1))
    print(apple_data)
    apple_data.to_csv('/mnt/c/Users/oscar/Documents/Stocks/automatic_quandl/AAPL.csv', encoding='utf-8')
