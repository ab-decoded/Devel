from testing.models import Templates
from django.contrib.auth.models import User
from django import forms

class TemplatesForm(forms.ModelForm):
    class Meta:
        model = Templates
        fields = ('userId','htmlCode','pub_date','description','name','slug')