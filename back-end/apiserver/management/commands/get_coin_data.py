import json
from django.core.management.base import BaseCommand

from repos.github_api import get_coin_data


class Command(BaseCommand):
    help = 'Returns the Github data of a particular coin'

    def add_arguments(self, parser):
        parser.add_argument('file_name_in', nargs='+', type=str)
        parser.add_argument('file_name_out', nargs='+', type=str)

    def handle(self, *args, **options):

        file_name_in = options['file_name_in'][0]
        file_name_out = options['file_name_out'][0]

        f = open(file_name_in, 'r')
        lines = f.readlines()

        with open(file_name_out, 'w') as ff:
            ff.write("[")
            for line in lines:
                if line == "\n": continue
                i, coin_name, coin_id, rank = line.strip().split(",")
                print 'processing {0}, {1}'.format(i, coin_name)
                if coin_id == '':
                    continue
                res = get_coin_data(coin_name, coin_id, rank)
                ff.write(json.dumps(res) + ",")
            ff.write("]")
