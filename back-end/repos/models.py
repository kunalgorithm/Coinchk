from __future__ import unicode_literals

from django.db import models


class CoinResult(models.Model):
    coin_id = models.CharField(max_length=10, primary_key=True)
    coin_name = models.CharField(max_length=50, blank=False)
    is_open_sourced = models.BooleanField(default=False)
    forked = models.BooleanField(default=False)
    rank = models.IntegerField(blank=False, db_index=True)
    github_id = models.CharField(max_length=100, blank=True)
    github_link = models.CharField(max_length=1000, blank=True)

    total_contributors = models.IntegerField(default=0)

    readme_exists = models.BooleanField(default=False)
    readme_num_lines = models.IntegerField(default=0)

    num_contributors = models.IntegerField(default=0)
    latest_commits = models.DateField(blank=True)
    latest_pr = models.DateField(blank=True)
    num_open_issues = models.IntegerField(default=0)
    num_stars = models.IntegerField(default=0)
    num_watchers = models.IntegerField(default=0)
    num_forks = models.IntegerField(default=0)
