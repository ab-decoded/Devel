from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Templates(models.Model):
    userId = models.ForeignKey(User)
    htmlCode = models.TextField()
    pub_date = models.DateTimeField('date published')
    description=models.CharField(max_length=100)
    name=models.CharField(max_length=50)
    slug=models.CharField(max_length=100,unique=True,primary_key=True)
    def __unicode__(self):
    	return self.name
    def was_published_recently(self):
    	return self.pub_date>=timezone.now()-datetime.timedelta(days=1)



