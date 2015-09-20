from django.db import models
from django.utils import timezone

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
    # General
    id = models.CharField(max_length=80, unique=True, primary_key=True) # from LinkedIn
    name = models.CharField(max_length=200)
    last_updated = models.DateTimeField()

    # LinkedIn
    website = models.CharField(max_length=500)
    industry = models.CharField(max_length=500)
    locations = models.TextField()#SeparatedValuesField()
    ticker_symbol = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    logo_url = models.TextField()

    # Google
    news = models.TextField()

    def save(self, *args, **kwargs):
        '''
        On save update timestamps
        :param args:
        :param kwargs:
        :return:
        '''
        self.last_updated = timezone.now()
        return super(Company, self).save(*args, **kwargs)

class Profile(models.Model):
    user_id = models.CharField(max_length=80, unique=True, primary_key=True)

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    email = models.EmailField(unique=True)

    summary = models.CharField(max_length=500)
    #relevant_skills = models.TextField(default='{}')
    industry = models.CharField(max_length=40)
    location_name = models.CharField(max_length=255)

class Experience(models.Model):
    summary = models.TextField()
    expressed_skills = models.TextField(default='{}')

