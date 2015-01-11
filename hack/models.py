from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    phone = models.CharField(max_length = 30)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Class(models.Model):
	cid = models.CharField(max_length=50, default="Empty Class")

class Request(models.Model):
    cls = models.ForeignKey(Class)
    user = models.ForeignKey(User)
    time = models.DecimalField(decimal_places=2, max_digits=5)
    people = models.IntegerField()

class Session(models.Model):
	length = models.IntegerField(default=0)
	start = models.DateField()
	location = models.CharField(max_length = 100)