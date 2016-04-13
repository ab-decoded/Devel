import json
from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from .models import Mockup,Template
import os,time
from django.utils import timezone


def cleanHTML(temp):
	removeSet={'paint-area','paint-area--text','edit-area','edit-area--div','edit-area--text','edit-area--table','selected-area'}
	for word in removeSet:
		if word in temp:
			temp=temp.replace(word,"")
	return ' '.join(temp.split())

def index(request):
	return render(request,'yolo/index.html')

# def insertImage(request):
# 	if request.method=="POST":


def choose(request):
	if request.method=='POST':
		data=request.POST.dict()
		print data['type']
		print data['mockupId']
		print data['slug']
		if data['type']=='mockup':
			if data['mockupId'] is not None and data['slug'] is not None:
				# mockupSelectedHTML=Mockup.objects.values('htmlCode').filter(id=data['mockupId'])
				# print mockupSelected[0]['htmlCode']
				mockup=Mockup.objects.filter(id=data['mockupId']).values()[0];
				if Template.objects.filter(userId=request.user,slug=data['slug']).exists():
					return HttpResponse(json.dumps({'message':'You already own the URL. Please select a new one.','success':False}))
				else:
					x=Template(name=data['name'],slug=data['slug'],description=data['description'],htmlCode=mockup['htmlCode'],userId=request.user,pub_date=timezone.now())
					x.mockup_id=mockup['id']
					lol=mockup['htmlCode']
					print lol
					x.cleanedHtml=cleanHTML(lol)
					x.save()
					print 'working'
					return HttpResponse(json.dumps({'message':'Successfully created the template.','template':{'user':x.userId.username,'name':x.name,'slug':x.slug,'description':x.description},'success':True}))
		# return HttpResponse('yolo')
	if(request.user.is_authenticated()):
		mockups = Mockup.objects.defer('htmlCode').all()
		templates = Template.objects.defer('htmlCode','cleanedHtml').filter(userId=request.user).all()
		return render(request,'yolo/choose.html',{'mockups':mockups,'templates':templates})
	else:
		messages.error(request,"Please sign-in to continue!")
		return HttpResponseRedirect('/sign-in')
def deleteTemplate(request,slug):
	if request.method=='POST':
		data=request.POST.dict()
		Template.objects.filter(slug=data['slug']).delete()
		return HttpResponse('Successfully Deleted'); 

# def userTemplates(request):
''' For GET request- Currently not used!!! '''
# 	if request.method=='GET':
# 		data=list(Template.objects.filter(userId=request.user).values('slug','name','description'))
# 		print data
# 		return HttpResponse(json.dumps({'templates':data}));


def editor(request,slug):
	# print os.chdir()
	# fn = os.path.join(settings.PROJECT_ROOT, '../yolo/templates/yolo/editor/mockup.html');
	# mockup = open(fn)
	t=Template.objects.get(slug=slug);
	if request.method=='POST':
		t.htmlCode=request.POST.dict()['htmlCode']
		removeSet={'paint-area','paint-area--text','edit-area','edit-area--div','edit-area--text','edit-area--table','selected-area'}
		x=t.htmlCode
		t.cleanedHtml=cleanHTML(x)
		t.save()
	# return render(request,'testing/bewde.html',{'template':t})
	return render(request,'yolo/editor/editor.html',{'template':t})

def showcase(request,username,slug):
	user=User.objects.get(username=username)
	template=get_object_or_404(Template,userId_id=user.id,slug=slug)
	print template
	return render(request,'yolo/showcase.html',{'template':template})

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



# def handler404(request):
#     response = render(request,'yolo/partials/404.html')
#     response.status_code = 404
#     return response
