import json
from django.utils import timezone
from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import TemplatesForm
from .models import Templates
def abbe(request):
	if request.method=='POST':
		data=request.POST.copy()
		data['userId']=request.user.id
		data['pub_date']=timezone.now()
		template=TemplatesForm(data)
		template.save()
		# data.username=request.user.get_userid()
		print data
	return render(request,'testing/abbe.html')

def bewde(request):
	t=Templates.objects.get(slug="ahem-ahem");
	return render(request,'testing/bewde.html',{'template':t})

