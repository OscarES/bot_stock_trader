import time
import random
import csv

data_dir = '/mnt/c/Users/oscar/Documents/Stocks/'

delay = 0.5  # (s)

holdings = {'Net Worth': 100,'Cash': 100, 'AAPL': 0}

dates = []
with open(data_dir + 'AAPL' + '.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        date = row[0]
        # print(date)
        if date != 'Date':
            dates.append(date)


def get_one_stock_price(ticker, date):
    with open(data_dir + ticker + '.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == date:
                price = float(row[1][2:])  # ($)
    return price


def update_prices(date):
    ticker = 'AAPL'
    price = get_one_stock_price(ticker, date)
    # price = 10 + random.random() * 5  # ($)
    updated_prices = {ticker: price}  # ($)
    return updated_prices


def buy(portfolio, ticker, ticker_price, amount):
    price = ticker_price * amount  # ($)
    if portfolio['Cash'] > price:
        portfolio[ticker] += amount
        portfolio['Cash'] -= price
        return portfolio
    else:
        return portfolio


def sell(portfolio, ticker, ticker_price, amount):
    if amount < portfolio[ticker]:
        sell_value = ticker_price * amount  # ($)
        portfolio['Cash'] += sell_value  # ($)
        portfolio[ticker] -= amount
        return portfolio
    else:
        return portfolio


def update_net_worth(portfolio, prices):
    net_worth = portfolio['Cash']  # ($)
    for ticker in prices:
        net_worth += portfolio[ticker] * prices[ticker]  # ($)

    portfolio['Net Worth'] = net_worth
    return portfolio

days_gone_by = 1  # warning 1 will mean the first date in dates
while True:
    print(dates[-days_gone_by])

    # load next day's opening values
    prices = update_prices(dates[-days_gone_by])
    print(prices)

    # trade
    if holdings['AAPL'] > 5:
        holdings = sell(holdings, 'AAPL', prices['AAPL'], 2)
    elif holdings['Cash'] > prices['AAPL']:
        holdings = buy(holdings, 'AAPL', prices['AAPL'], 1)

    # print wealth
    holdings = update_net_worth(holdings, prices)
    print(holdings)
    print()

    days_gone_by += 1
    # time.sleep(delay)
