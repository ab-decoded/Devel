import json
from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Mockup
import os,time


def index(request):
	return render(request,'yolo/index.html')

def choose(request):
	if request.method=='POST':
		data=request.POST.dict()
		print data['type']
		print data['mockupId']
		print data['slug']
		if data['type']=='mockup':
			if data['mockupId'] is not None and data['slug'] is not None:
				print 'working'

		# return HttpResponse('yolo')
	if(request.user.is_authenticated()):
		mockups = Mockup.objects.defer('htmlCode').all()
		# print mockups
		return render(request,'yolo/choose.html',{'mockups':mockups})
	else:
		messages.error(request,"Please sign-in to continue!")
		return HttpResponseRedirect('/sign-in')


def editor(request):
	# print os.chdir()
	fn = os.path.join(settings.PROJECT_ROOT, '../yolo/templates/yolo/editor/mockup.html');
	mockup = open(fn)
	# print mockup.read()
	return render(request,'yolo/editor/editor.html',{'mockup':mockup.read()})

def signup(request):
	# context=RequestContext(request)
	registered=False
	user_form=None
	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		if user_form.is_valid():
			user_form.clean_email()
			user=user_form.save()
			user.set_password(user.password)
			user.save()
			new_user=authenticate(username=user_form.cleaned_data['username'],password=user_form.cleaned_data['password'])
			login(request,new_user)
			messages.info(request,'Thank you for registering. You are now logged in!')
			registered=True
			# return HttpResponse(json.dumps({'errors': ''}))
		else:
			print json.dumps({'errors': user_form.errors})
			# return HttpResponse(json.dumps({'errors': user_form.errors}))
			# return render(request,'yolo/accounts/signup.html',{'registered':registered,'errors':user_form.errors})
	if user_form!=None:
		return render(request,'yolo/accounts/signup.html',{'registered':registered,'errors':user_form.errors})
	else:
		return render(request,'yolo/accounts/signup.html',{'registered':registered,'errors':None})

def signin(request):

    errors=[]
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request,'Successfully logged in.')
                return HttpResponseRedirect('/')
            else:
                errors.append("Your Account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            errors.append("Invalid login details supplied.")
    
    return render(request,'yolo/accounts/signin.html', {'errors':errors})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    messages.error(request,'Logged out. Missing you already')
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

