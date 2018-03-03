## Django initial setup

1. make a virtualenv (optional, but recommended)
2. run 'pip install -r requirements.txt' to install all python dependencies i.e. Django, requests, etc.

## How to run Django

1. run 'python manage.py runserver'

## How to fetch the names of all top N coins from coinmarketcap.com in JSON

1. run 'python manage.py get_top_coin_names N FILE_NAME'
where N = top N number of coins you want, FILE_NAME = where you want data to be dumped.
e.g. 'python manage.py get_top_coin_names 1000 top1000_coins.json'

