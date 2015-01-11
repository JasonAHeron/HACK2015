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
    time = models.FloatField()
    people = models.IntegerField()
    schedule = models.CharField(max_length= 999)

    def brit_dump(self):
        dct = eval(self.schedule)
        dct = dict((k.encode('ascii'), v) for (k, v) in dct.items())  
        dct['id'] = str(self.user.username)
        dct['minT'] = self.time
        dct['minP'] = self.people
        return dct


class Session(models.Model):
	length = models.IntegerField(default=0)
	start = models.DateField()
	location = models.CharField(max_length = 100)