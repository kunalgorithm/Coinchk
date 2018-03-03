import json
from django.core.management.base import BaseCommand

from repos.coinmarketcap_api import get_github_repo_id, get_coin_rankings


class Command(BaseCommand):
    help = 'Pulls the Github repo addresses and repo ids of top N coins from coinmarketcap.com ' \
           'and dumps to a file locally in JSON'

    def add_arguments(self, parser):
        parser.add_argument('num_coins', nargs='+', type=int)
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):

        num_coins = options['num_coins'][0]
        file_name = options['file_name'][0]

        print 'getting the repo addresses/ids of top {0} coins from coinmarketcap and dumping to file = {1}'.format(
            num_coins,
            file_name
        )
        coins = get_coin_rankings(0, num_coins)
        res_json = {}
        count = 0
        for coin_rank, coin_name in coins:
            repo_addr, repo_id = get_github_repo_id(coin_name)
            res_json[coin_name] = {
                "rank": coin_rank,
                "addr": repo_addr or '',
                "id": repo_id or ''
            }
            if count % 10 == 0:
                print 'has processed {0} repos..'.format(count)
            count += 1

        with open(file_name, 'w') as f:
            f.write(json.dumps(res_json))
