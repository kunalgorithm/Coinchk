import requests
from apiserver.settings import coinmarketcap_api, \
    COINMARKETCAP_DETAIL_PAGE_URL, GITHUB_ADDRESS_PREFIX


# Gets the list of coins ranked from @start to @limit
# each of which is of format (rank, coin_name)
# e.g. [(1, 'bitcoin'), (2, 'ethereum'), ...]
def get_coin_rankings(start, limit):
    res = coinmarketcap_api.ticker(start=start, limit=limit)

    def to_internal_rep(coin_data):
        return int(coin_data['rank']), coin_data['id']

    return map(to_internal_rep, res)


# Given a coin name, returns its github address if exists.
# None if does not exists.
def get_github_repo_id(coin_name):
    url_to_request = COINMARKETCAP_DETAIL_PAGE_URL.format(coin_name)
    try:
        details_page = requests.get(url_to_request).text
        if 'Source Code' not in details_page:
            print '{0} has no source code'.format(coin_name)
            return None, None
        try:
            starting_index = details_page.index(GITHUB_ADDRESS_PREFIX) - 1
        except ValueError:
            print '{0} uses bitbucket or something..'.format(coin_name)
            return None, None
        # +100 should be long enough
        substring = details_page[starting_index: starting_index + 100]
        end_index = substring[1:].index('"')
        repo_addr = details_page[starting_index + 1: starting_index + end_index + 1]
        if repo_addr.endswith('/'):
            repo_addr = repo_addr[:-1]
        repo_id = repo_addr.split(GITHUB_ADDRESS_PREFIX)[1]
        return repo_addr, repo_id

    except requests.RequestException:
        print 'for {0}, requests failed..'.format(coin_name)
        return None, None
