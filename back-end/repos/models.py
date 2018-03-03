from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Coin(models.Model):
    coin_id = models.CharField(max_length=10, primary_key=True)
    coin_name = models.CharField(max_length=50, blank=False)

    # required fields
    github_link = models.TextField(blank=False)
    official_site_link = models.TextField(blank=False)

    total_contributors = models.IntegerField(blank=False)
    active_contributors = models.IntegerField(blank=False)

    read_me_score = models.IntegerField(default=0)
    issues_score = models.IntegerField(default=0)
    issues_open = models.IntegerField(blank=False)
    issues_closed = models.IntegerField(blank=False)

    pr_score = models.IntegerField(default=0)
    pr_open = models.IntegerField(blank=False)
    pr_closed = models.IntegerField(blank=False)
    pr_merged = models.IntegerField(blank=False)

    # optional fields

    def __str__(self):
        return "coin_id={0}, name={1}".format(self.coin_id, self.coin_name)
