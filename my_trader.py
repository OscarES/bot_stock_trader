import time
import random
import csv
import math
from os import listdir
from os.path import isfile, join
import operator

"""Trading bot that trades with knowledge of future prices"""

data_dir = '/mnt/c/Users/oscar/Documents/Stocks/'

delay = 0.5  # (s)

holdings = {'Net Worth': 1000000,'Cash': 1000000}

ticker_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
tickers = [f[:-4] for f in ticker_files if f[-4:] == '.csv']

for ticker in tickers:
    holdings[ticker] = 0

dates = []
with open(data_dir + 'AAPL' + '.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        date = row[0]
        # print(date)
        if date != 'Date':
            dates.append(date)


def get_one_stock_price(ticker, date):
    """Gets the price of a stock at a certain date"""
    with open(data_dir + ticker + '.csv', 'r') as f:
        reader = csv.reader(f)
        price = 0  # ($)
        for row in reader:
            if row[0] == date:
                price = float(row[1][2:])  # ($)
    return price


def update_prices(date):
    """Update the list of stock prices"""
    updated_prices = {}
    for ticker in tickers:
        price = get_one_stock_price(ticker, date)
        # price = 10 + random.random() * 5  # ($)
        updated_prices[ticker] = price  # ($)
    return updated_prices


def buy(portfolio, ticker, ticker_price, amount):
    """Buys stocks for the bot's portfolio"""
    price = ticker_price * amount  # ($)
    if portfolio['Cash'] > price:
        portfolio[ticker] += amount
        portfolio['Cash'] -= price
        return portfolio
    else:
        return portfolio


def buy_max(portfolio, ticker, ticker_price):
    """Buys all in on one stock"""
    if ticker_price == 0:
        return portfolio
    max_amount = math.floor(portfolio['Cash'] / ticker_price)
    return buy(portfolio, ticker, ticker_price, max_amount)


def sell(portfolio, ticker, ticker_price, amount):
    """Sells stocks from the bot's portfolio"""
    if amount <= portfolio[ticker]:
        sell_value = ticker_price * amount  # ($)
        portfolio['Cash'] += sell_value  # ($)
        portfolio[ticker] -= amount
        return portfolio
    else:
        return portfolio


def sell_max(portfolio, ticker, ticker_price):
    """Sells all stocks of one ticker in the bot's portfolio"""
    max_amount = portfolio[ticker]
    return sell(portfolio, ticker, ticker_price, max_amount)


def sell_all(portfolio, prices):
    """Sells all stocks in the bot's portfolio"""
    for ticker in tickers:
        portfolio = sell_max(portfolio, ticker, prices[ticker])
    return portfolio


def update_net_worth(portfolio, prices):
    """Updates the net worth of the bot"""
    net_worth = portfolio['Cash']  # ($)
    for ticker in prices:
        net_worth += portfolio[ticker] * prices[ticker]  # ($)

    portfolio['Net Worth'] = net_worth
    return portfolio


# Main script
days_gone_by = 1  # warning 1 will mean the first date in dates
while len(dates) >= days_gone_by:
    print(dates[-days_gone_by])

    # load next day's closing values
    prices = update_prices(dates[-days_gone_by])
    print(prices)

    # trade
    if len(dates) > days_gone_by + 1:
        tomorrows_prices = update_prices(dates[-(days_gone_by + 1)])
        arbitrages = {k : tomorrows_prices[k] - prices[k] for k in prices.keys()}
        holdings = sell_all(holdings, prices)
        best_arbitrage_ticker = max(arbitrages.items(), key=operator.itemgetter(1))[0]
        # print('Arbitrages: {}'.format(arbitrages))
        if arbitrages[best_arbitrage_ticker] > 0:
            holdings = buy_max(holdings, best_arbitrage_ticker, prices[best_arbitrage_ticker])


    # if holdings['AAPL'] > 5:
    #     holdings = sell_max(holdings, 'AAPL', prices['AAPL'])
    # elif holdings['Cash'] > prices['AAPL']:
    #     holdings = buy_max(holdings, 'AAPL', prices['AAPL'])

    # print wealth
    holdings = update_net_worth(holdings, prices)
    print(holdings)
    print()

    days_gone_by += 1
    # time.sleep(delay)
