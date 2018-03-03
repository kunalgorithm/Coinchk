import json
from django.core.management.base import BaseCommand, CommandError

from repos.coinmarketcap_api import get_coin_rankings


class Command(BaseCommand):
    help = 'Pulls the list of top N coins from coinmarketcap.com and dumps to a file locally in JSON'

    def add_arguments(self, parser):
        parser.add_argument('num_coins', nargs='+', type=int)
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):

        num_coins = options['num_coins'][0]
        file_name = options['file_name'][0]

        print 'getting top {0} coins from coinmarketcap and dumping to file = {1}'.format(
            num_coins,
            file_name
        )
        coins = get_coin_rankings(0, num_coins)
        res_json = {}

        for coin in coins:
            res_json[coin[1]] = coin[0]

        with open(file_name, 'w') as f:
            f.write(json.dumps(res_json))
