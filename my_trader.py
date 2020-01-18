import time

data_dir = '/mnt/c/Users/Oscar/Stocks'

delay = 0.5  # (s)

holdings = {'Net Worth': 100,'Cash': 100, 'APPL': 0}


def update_prices():
    updated_prices = {'APPL': 10}
    return updated_prices


def buy(portfolio, ticker, ticker_price, amount):
    price = ticker_price * amount  # ($)
    if portfolio['Cash'] > price:
        portfolio[ticker] += amount
        portfolio['Cash'] -= price
        return portfolio
    else:
        return portfolio


def sell(portfolio, ticker, amount):
    return


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
    if holdings['Cash'] > prices['APPL']:
        holdings = buy(holdings, 'APPL', prices['APPL'], 1)

    # print wealth
    holdings = update_net_worth(holdings, prices)
    print(holdings)

    time.sleep(delay)
