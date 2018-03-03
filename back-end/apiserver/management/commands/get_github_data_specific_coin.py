import json
from django.core.management.base import BaseCommand

from repos.github_api import get_coin_data


class Command(BaseCommand):
    help = 'Returns the Github data of a particular coin'

    def add_arguments(self, parser):
        parser.add_argument('coin_name', nargs='+', type=str)
        parser.add_argument('id', nargs='+', type=str)
        parser.add_argument('rank', nargs='+', type=int)
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):

        coin_name = options['coin_name'][0]
        id = options['id'][0]
        rank = options['rank'][0]
        file_name = options['file_name'][0]

        print self.help + ' for {0}'.format(coin_name)

        res = get_coin_data(coin_name, id, rank)
        print res

        with open(file_name, 'w') as f:
            f.write(json.dumps(res))
