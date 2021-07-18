import cbpro
import time

secret = 'Put api secret here'
key = 'Put api key here'
phrase = 'Put phrase here'

#####Public/Private Client Set-up#####

public_client = cbpro.PublicClient()

# Remove api_url for real trading

auth_client = cbpro.AuthenticatedClient(
    key, secret, phrase, api_url="https://api-public.sandbox.pro.coinbase.com")

#####Custom Setttings#####

# Smallest cryptocurrency buy/sell size is .001

crypto_size = .1

account_investment_funds_percent = .2

sell_with = 'BTC'

buy_with = 'USD'

profit_margin = .02

#####Main Program#####

bought_orders = 0

total_orders_price = 0

sell_price = 5000000000

buy_fees = 0

sell_fees = 0

accounts = auth_client.get_accounts()

for x in range(len(accounts)):
    if accounts[x]['currency'] == f'{buy_with}':
        available_funds = float(accounts[x]['available'])
        funds_id = accounts[x]['id']
        balance_funds = float(accounts[x]['balance'])
    if accounts[x]['currency'] == f'{sell_with}':
        available_crypto_funds = float(accounts[x]['available'])
        crypto_funds_id = accounts[x]['id']
        crypto_balance_funds = float(accounts[x]['balance'])

current_price = float(public_client.get_product_ticker(
    product_id=f'{sell_with}'+f'-{buy_with}')['price'])*crypto_size

while(True):

    time.sleep(5)

    if current_price > sell_price+(sell_price*profit_margin):

        auth_client.place_market_order(
            size=f'{crypto_size*bought_orders}', side='sell', product_id=f'{sell_with}-{buy_with}')

        bought_orders = 0

        total_orders_price = 0

        sell_price = 5000000000

        buy_fees = 0

        for x in range(len(accounts)):
            if accounts[x]['currency'] == f'{buy_with}':
                available_funds = float(accounts[x]['available'])
                balance_funds = accounts[x]['balance']

    elif total_orders_price >= balance_funds*account_investment_funds_percent:
        current_price = float(public_client.get_product_ticker(
            product_id=f'{sell_with}-{buy_with}')['price'])*crypto_size
    else:
        crypto_bought = auth_client.place_market_order(
            size=f'{crypto_size}', side='buy', product_id=f'{sell_with}-{buy_with}')

        order_value = auth_client.get_order(crypto_bought['id'])[
            'executed_value']

        bought_orders += 1

        total_orders_price += float(order_value)

        buy_fees += float(auth_client.get_order(crypto_bought['id'])[
            'fill_fees'])

        sell_price = (total_orders_price/bought_orders) + \
            buy_fees

        print(sell_price)

        available_funds = float(auth_client.get_account(funds_id)[
            'available'])
