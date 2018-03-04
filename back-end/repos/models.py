from __future__ import unicode_literals

from django.db import models


class CoinResult(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    coin_name = models.CharField(max_length=50, blank=False)
    is_open_sourced = models.BooleanField(default=False)
    forked = models.BooleanField(default=False)
    rank = models.IntegerField(blank=False, db_index=True)
    github_id = models.CharField(max_length=100, blank=True)
    github_link = models.CharField(max_length=1000, blank=True)

    readme_exists = models.BooleanField(default=False)
    readme_num_lines = models.IntegerField(default=0)
    dev_score = models.FloatField(default=0)
    num_contributors = models.IntegerField(default=0)
    latest_commits = models.DateField(null=True, blank=True)
    bin_commits = models.BooleanField(default=False)
    bin_prs = models.BooleanField(default=False)
    latest_pr = models.DateField(null=True, blank=True)
    num_open_issues = models.IntegerField(default=0)
    num_stars = models.IntegerField(default=0)
    num_watchers = models.IntegerField(default=0)
    num_forks = models.IntegerField(default=0)
