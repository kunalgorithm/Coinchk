from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

from repos.models import Coin


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
    return {
    }


def api_details(request, coin_id):
    try:
        m = Coin.objects.get(coin_id=coin_id)
    except ObjectDoesNotExist:
        r = JsonResponse({
            'error': "Coin with id '{}' was not found.".format(coin_id)
        })
        r.status_code = 404
        return r

    return JsonResponse(_details(m))
