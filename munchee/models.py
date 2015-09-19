from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# using django's default user model

class Activity(models.Model):
	verb = models.CharField(max_length=30)
	noun = models.CharField(max_length=30)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	up_to_date = models.BooleanField(default=True)
	mean = models.FloatField(default=0.0)
	percentile_80 = models.FloatField(default=0.0)
	hist = models.TextField(default="[[0,0,None]]")
	num_times = models.IntegerField(default=0)
	sources = models.TextField(default='[["source","contribution"],["users",0]]')  # list of lists for google charts
	source_urls = models.TextField(default='[]')  # list of urls
	def get_absolute_url(self):
		return reverse('activity', kwargs={'verb':self.verb, 'noun':self.noun})
	def __str__(self):
		return " ".join([self.verb, self.noun])
	class Meta:
		unique_together = ("verb", "noun")
		verbose_name_plural = "Activities"
		
class Time(models.Model):
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	activity = models.ForeignKey(Activity)  # each time belongs to an activity
	user = models.ForeignKey(User)  # each time belongs to a user
	seconds = models.FloatField(null=True)  # time measured in seconds
	def __str__(self):
		return ":".join([str(self.activity), str(self.seconds)])

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	watching = models.ManyToManyField("self", symmetrical=False)
	description = models.TextField(default="")

class Notification(models.Model):
	CHALLENGE = 0
	CATEGORIES = (
		(CHALLENGE, "Challenge"),
	)
	sender = models.ForeignKey(User, related_name='sent_notification_set')
	recipient = models.ForeignKey(User, related_name='received_notification_set')
	category = models.PositiveSmallIntegerField(choices=CATEGORIES)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	read = models.BooleanField(default=False)
	link = models.TextField(null=True)
	activity = models.ForeignKey(Activity, null=True)
	time = models.ForeignKey(Time, null=True)
