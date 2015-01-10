from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Class(models.Model):
	cid = models.CharField(max_length=50, default="Empty Class")


class Request(models.Model):
	cls = models.ForeignKey(Class)

