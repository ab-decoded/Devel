from django.contrib import admin
from .models import UserProfile,Mockup,Template

admin.site.register(UserProfile)
admin.site.register(Mockup)
admin.site.register(Template)