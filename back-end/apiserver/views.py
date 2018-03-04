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

    req = 30 if coin.rank <= 100 else 15
    # commit_day_diff = (datetime.now() - coin.latest_commits).days
    # pr_day_diff = (datetime.now() - coin.latest_pr).days

    issues_req = 1000 if coin.rank <= 100 else 100

    return {
        'name': coin.coin_name,
        'is_open_sourced': 1 if coin.is_open_sourced else 0,
        'dev_score': coin.dev_score,
        'is_forked': 1 if coin.forked else 0,
        'is_readme_good': 1 if coin.readme_exists and coin.readme_num_lines >= 50 else 0,
        'is_contributor_active': 1 if coin.num_contributors >= req else 0,
        'is_development_recent': 1 if coin.bin_commits or coin.bin_prs else 0,
        'is_open_issues_small': 1 if coin.num_open_issues <= issues_req else 0,
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
