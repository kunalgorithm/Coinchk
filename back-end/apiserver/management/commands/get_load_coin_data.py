import json
from django.core.management.base import BaseCommand

from repos.coinmarketcap_api import get_coin_rankings
from repos.models import CoinResult


class Command(BaseCommand):
    help = 'Pulls the list of top N coins from coinmarketcap.com and dumps to a file locally in JSON'

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        file_name = options['file_name'][0]

        f = open(file_name, 'r')
        d = f.readlines()

        for l in d:
            # print l
            l = l.strip().split(',')
            m = CoinResult(
                coin_name=l[0],
                github_id=l[1],
                rank=int(l[2])
            )
            m.save()


        # coins = get_coin_rankings(0, num_coins)
        # res_json = {}

        # for coin in coins:
        #     res_json[coin[1]] = coin[0]
        #
        # with open(file_name, 'w') as f:
        #     f.write(json.dumps(res_json))
