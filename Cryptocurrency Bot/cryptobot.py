import tweepy
from os import environ
from time import sleep
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

load_dotenv()
cg = CoinGeckoAPI()
def create_API():

    keys = {
        'CONSUMER_KEY':         environ['CONSUMER_KEY'],
        'CONSUMER_SECRET':      environ['CONSUMER_SECRET'],
        'ACCESS_TOKEN':         environ['ACCESS_TOKEN'],
        'ACCESS_TOKEN_SECRET':  environ['ACCESS_TOKEN_SECRET']
    }

    client = tweepy.Client(
        consumer_key=keys['CONSUMER_KEY'],
        consumer_secret=keys['CONSUMER_SECRET'],
        access_token=keys['ACCESS_TOKEN'],
        access_token_secret=keys['ACCESS_TOKEN_SECRET']
    )

    return client

def get_price_last_hour(coin, interval):
    response = cg.get_coin_market_chart_by_id(id=f'{coin}', vs_currency='gbp', days='7')
    price_last_hour = response['prices'][0][1]
    return price_last_hour

def get_price(coin):
    price = cg.get_price(ids=f"{coin}", vs_currencies='usd')
    return price[f"{coin}"]['usd']

def generate_status(coin, price, price_1h, interval):
    price_change = round(price - price_1h, 2)
    change_percent = round(((price/price_1h) * 100) - 100, 2)

    emoji = "🔴⬇️" if change_percent < 0 else "🟢⬆️"

    status = f"{coin.capitalize()}: ${price} ({change_percent}% | ${price_change} {emoji})\n"

    return status

def big_status():
    coins = [
        'bitcoin', 'ethereum', 'solana',
        'cardano'
    ]

    interval = 'hourly'

    status = f"Crypto Stats (Last Hour)\n\n"

    for coin in coins:
        price = float(get_price(coin))
        sleep(6)
        price_1h = float(get_price_last_hour(coin, interval))

        status += generate_status(coin, price, price_1h, interval)

    status += f"\n#cryptonews #crypto #trading"

    for coin in coins:
        status += f" #{coin}"

    return status

def tweet_status(api, message):
    print(message)
    api.create_tweet(text=message)
    print(f'Tweeted')

def main():
    
    API = create_API()

    status = big_status()

    tweet_status(API, status)

while True:
    main()
    sleep(3600)
