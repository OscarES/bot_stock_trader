import time
import random

data_dir = '/mnt/c/Users/Oscar/Stocks'

delay = 0.5  # (s)

holdings = {'Net Worth': 100,'Cash': 100, 'APPL': 0}


def update_prices():
    updated_prices = {'APPL': 10 + random.random() * 5}  # ($)
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


while True:
    # load next day's opening values
    prices = update_prices()

    # trade
    if holdings['APPL'] > 5:
        holdings = sell(holdings, 'APPL', prices['APPL'], 2)
    elif holdings['Cash'] > prices['APPL']:
        holdings = buy(holdings, 'APPL', prices['APPL'], 1)

    # print wealth
    holdings = update_net_worth(holdings, prices)
    print(holdings)

    time.sleep(delay)
