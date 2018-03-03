import json
from django.core.management.base import BaseCommand

from apiserver.settings import github_object, GITHUB_ADDRESS_PREFIX
from repos.coinmarketcap_api import get_github_repo_id, get_coin_rankings

from github import UnknownObjectException

class Command(BaseCommand):
    help = 'Grabs the repo address data from a local file and cleans them up ' \
           'i.e. for addresses that refer to organizations, find the addresses of actual coin repos ' \
            '(the repositories with the most number of stars'

    def add_arguments(self, parser):
        parser.add_argument('file_name_in', nargs='+', type=str)
        parser.add_argument('file_name_out', nargs='+', type=str)

    def handle(self, *args, **options):

        file_name_in = options['file_name_in'][0]
        file_name_out = options['file_name_out'][0]

        print self.help

        res_json = {}
        count = 0

        with open(file_name_in, 'r') as f:
            coin_data = json.loads(f.read())
            for coin_name, coin_data in coin_data.iteritems():
                print coin_name
                coin_github_id = coin_data['id']
                repo = github_object.get_repo(coin_github_id)
                try:
                    fn = repo.full_name
                    res_json[coin_name] = {
                        "rank": coin_data['rank'],
                        "addr": coin_data['addr'] or '',
                        "id": coin_data['id'] or ''
                    }

                except UnknownObjectException:
                    if coin_data['id'] == "":
                        res_json[coin_name] = {
                            "rank": coin_data['rank'],
                            "addr": coin_data['addr'] or '',
                            "id": coin_data['id'] or ''
                        }
                    else:
                        # the repo address is an organization address!
                        try:
                            org = github_object.get_organization(coin_github_id)
                            repos = list(org.get_repos())
                            if len(repos) == 0:
                                res_json[coin_name] = {
                                    "rank": coin_data['rank'],
                                    "addr": '',
                                    "id": ''
                                }
                            else:
                                best_repo = None
                                most_num_stars = -1
                                for repo in repos:
                                    if best_repo is None:
                                        best_repo = repo
                                        most_num_stars = repo.stargazers_count
                                    else:
                                        if repo.stargazers_count > most_num_stars:
                                            best_repo = repo
                                            most_num_stars = repo.stargazers_count

                                res_json[coin_name] = {
                                    "rank": coin_data['rank'],
                                    "addr": GITHUB_ADDRESS_PREFIX + best_repo.full_name,
                                    "id": best_repo.full_name
                                }
                        except UnknownObjectException:
                            res_json[coin_name] = {
                                "rank": coin_data['rank'],
                                "addr": coin_data['addr'] or '',
                                "id": coin_data['id'] or ''
                            }

                if count % 10 == 0:
                    print 'has processed {0} repos..'.format(count)
                count += 1

        with open(file_name_out, 'w') as f:
            f.write(json.dumps(res_json))
            f.close()
