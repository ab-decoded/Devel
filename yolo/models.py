# Change your models (in models.py).
# Run python manage.py makemigrations to create migrations for those changes
# Run python manage.py migrate to apply those changes to the database.
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    # picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Mockup(models.Model):
    author = models.CharField(max_length=200)
    htmlCode = models.TextField()
    pub_date = models.DateTimeField('date published')
    description=models.CharField(max_length=100)
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to='mockups',null=True)
    def __unicode__(self):
        return self.name
    def was_published_recently(self):
        return self.pub_date>=timezone.now()-datetime.timedelta(days=1)


class Template(models.Model):
    userId = models.ForeignKey(User)
    mockup=models.ForeignKey(Mockup,null=True)
    htmlCode = models.TextField()
    cleanedHtml = models.TextField()
    pub_date = models.DateTimeField('date published')
    description=models.CharField(max_length=100)
    name=models.CharField(max_length=50)
    slug=models.CharField(max_length=100,unique=True,primary_key=True)
    temporary=models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Template_images(models.Model):
    image=models.ImageField(upload_to='templateImages')
    template=models.ForeignKey(Template,null=True)
    def __unicode__(self):
        return self.image.url