import json
from django.core.management.base import BaseCommand

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
            try:
                m = CoinResult.objects.filter(coin_name=l)[0]
                m.dev_score = int(d[l])
                m.save()
            except:
                continue
