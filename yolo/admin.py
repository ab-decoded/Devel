from django.contrib import admin
from .models import Question,UserProfile

admin.site.register(Question)

admin.site.register(UserProfile)