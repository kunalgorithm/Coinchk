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
        d = json.loads(f.read())

        for l in d:
            m = CoinResult.objects.filter(coin_name=l)[0]
            m.bin_commits = True if d[l]['under development'] else False
            m.save()
