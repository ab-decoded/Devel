import json
from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .forms import UserForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import os

def index(request):
	return render(request,'yolo/index.html')

def editor(request):
	# print os.chdir()
	mockup = open('/home/ab/Desktop/flaskapp/devel_main/yolo/templates/yolo/editor/mockup.html')
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

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
