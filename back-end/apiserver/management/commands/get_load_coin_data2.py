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

            m = CoinResult.objects.filter(coin_name=l['name'])[0]
            m.num_contributors = l['num_contributors']
            m.num_stars = l['num_stars']
            m.num_watchers = l['num_watchers']
            m.num_forks = l['num_forks']
            m.is_open_sourced = True
            m.forked = True if l['forked'] == 1 else False
            m.readme_exists = True if l['readme_exists'] else False
            m.readme_num_lines = l['readme_linecount']
            m.open_issues = l['num_issues_open']
            m.num_contributors = l['num_contributors']
            m.github_link = 'https://github.com/{0}'.format(l['id'])
            m.save()
