from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime

from repos.models import CoinResult


def main(request):
    return render(request, "index.html")


def _overview(coin):
    return {
        'coin_id': int(coin.coin_id),
        'coin_name': coin.coin_name,
        'github_link': coin.github_link,
        'readme_score': coin.readme_score,
        'num_contributors': coin.active_contributors,
        'issues_score': coin.issues_score,
        'pr_score': coin.pr_score
    }


def _details(coin):

    req = 15 if coin.rank <= 100 else 10
    # commit_day_diff = (datetime.now() - coin.latest_commits).days
    # pr_day_diff = (datetime.now() - coin.latest_pr).days

    issues_req = 1000 if coin.rank <= 100 else 100

    return {
        'name': coin.coin_name,
        'is_open_sourced': True if coin.is_open_sourced else False,
        'is_forked': True if coin.forked else False,
        'is_readme_good': True if coin.readme_exists and coin.readme_num_lines >= 100 else False,
        'is_contributor_active': True if coin.num_contributors >= req else False,
        'is_development_recent': coin.bin_commits or coin.bin_prs,
        'is_open_issues_small': True if coin.num_open_issues <= issues_req else False,
        'num_stars': coin.num_stars,
        'num_watchers': coin.num_watchers,
        'num_forks': coin.num_forks
    }


def api_range(request):

    from_ = request.GET['from']
    to_ = request.GET['to']

    coin_results = CoinResult.objects.filter(rank__gte=from_, rank__lte=to_)

    res = {}
    for coin in coin_results:
        res[coin.rank] = _details(coin)

    return JsonResponse(res)

#
# def api_details(request, coin_id):
#     try:
#         m = Coin.objects.get(coin_id=coin_id)
#     except ObjectDoesNotExist:
#         r = JsonResponse({
#             'error': "Coin with id '{}' was not found.".format(coin_id)
#         })
#         r.status_code = 404
#         return r
#
#     return JsonResponse(_details(m))
