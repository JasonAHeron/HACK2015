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

class Schedule(models.Model):
    user = models.ForeignKey(User)
    schedule = models.CharField(max_length= 999)

class Session(models.Model):
    length = models.IntegerField(default=0)
    start = models.IntegerField(default=0)

class Request(models.Model):
    session = models.ForeignKey(Session, null=True)
    cls = models.ForeignKey(Class)
    user = models.ForeignKey(User)
    time = models.FloatField()
    people = models.IntegerField()
    phone = models.CharField(max_length= 30)
    schedule = models.CharField(max_length= 999)

    def brit_dump(self):
        overall = {}
        dct = eval(self.schedule)
        dct = dict((k.encode('ascii'), v) for (k, v) in dct.items())  
        overall['schedule'] = dct
        overall['id'] = str(self.user.username)
        overall['minT'] = self.time
        overall['minP'] = self.people
        overall['phone'] = self.phone
        #dct['phone'] = UserProfile.objects.filter(user=self.user).phone
        #print dct['phone']
        return overall
