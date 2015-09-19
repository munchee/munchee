from django.db import models
from munchee.custom import SeparatedValuesField

from datetime import datetime
# from django.utils import timezone
# from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User
# using django's default user model


# class Job(models.Model):
#   relevant_skills = models.TextField(default='{}')
#   company = models.ForeignKey(Company)
#   summary = models.TextField()
#   location = models.CharField(max_length=80)
#   position = models.CharField(max_length=80)

class Company(models.Model):
    name = models.CharField()
    last_updated = models.DateTimeField()
    summary = models.TextField()
    ticker_symbol = models.CharField(max_length=80)
    # id = models.CharField(max_length=80)

    relevant_skills = models.TextField(default="{}")
    links = SeparatedValuesField()
    positions = SeparatedValuesField()

    def update():
        # crawls relevant pages to update summary and positions if necessary
        last_updated = datetime.now()
        # update summary
        # update relevant skills
        # update links
        # update positions

class Profile(models.Model):
    name = models.CharField(max_length=80)

    relevant_skills = models.TextField(default='{}')
    interested_positions = SeparatedValuesField()

class Experience(models.Model):
    summary = models.TextField()
    expressed_skills = models.TextField(default='{}')
