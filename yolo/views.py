import json,os,time,zipfile,StringIO
from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.template import RequestContext
from .forms import UserForm,ImageForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from .models import Mockup,Template,Template_images
from django.utils import timezone

def cleanHTML(temp,removeSet):
	for word in removeSet:
		if word in temp:
			temp=temp.replace(word,"")
	# return ' '.join(temp.split())
	return temp.lstrip()
def index(request):
	return render(request,'yolo/index.html')

#HELL YEAHH!!!!!!!!!!!!!!!!!! Ho gaya BC
def downloadAsZip(request,username,slug):
	 # os.path.join(settings.PROJECT_ROOT, '../yolo/static/bowerComponents/dist/semantic.css');
	filenames=[os.path.join(settings.PROJECT_ROOT, '../yolo/static/bowerComponents/semantic/dist/semantic.min.css'),os.path.join(settings.PROJECT_ROOT, '../yolo/static/bowerComponents/jquery/dist/jquery.min.js'),os.path.join(settings.PROJECT_ROOT, '../yolo/static/bowerComponents/semantic/dist/semantic.min.js')]
	zip_subdir="static"
	zip_filename="project.zip"
	s = StringIO.StringIO()
	user=User.objects.get(username=username)
	temp=Template.objects.get(userId=user,slug=slug)
	# The zip compressor
	zf = zipfile.ZipFile(s, "w")

	for fpath in filenames:
		# Calculate path for file in zip
		fdir, fname = os.path.split(fpath)
		zip_path = os.path.join(zip_subdir, fname)
		# Add file, at correct path
		zf.write(fpath, zip_path)

	images=Template_images.objects.filter(template=temp).values()
	for image in images:
		print image
		fdir,fname=os.path.split(os.path.join(settings.PROJECT_ROOT,'../devel_main/media/'+image['image']))
		zip_path = os.path.join("static/templateImages",fname)
		image_path=os.path.join(settings.PROJECT_ROOT,'../devel_main/media/'+image['image'])
		if(os.path.exists(image_path)):
			f=open(image_path)
			zf.writestr(zip_path,f.read())
			f.close()

	with open(os.path.join(settings.PROJECT_ROOT,'../yolo/static/header.html'), 'r') as myfile:
	    data=myfile.read()
	print temp.cleanedHtml
	data+=temp.cleanedHtml.replace('/media','./static')
	with open(os.path.join(settings.PROJECT_ROOT,'../yolo/static/footer.html'), 'r') as myfile:
	    footer_data=myfile.read()
	data+=footer_data
	# zf.writestr("index.html",temp.cleanedHtml.encode('utf-8'))
	zf.writestr("index.html",data.encode('utf-8'))
	# Must close zip for all contents to be written
	zf.close()
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
	   # ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp

def insertImage(request):
	if request.method=="POST":
		form=ImageForm(request.POST,request.FILES)
		print request.POST
		if form.is_valid():
			m=Template_images()
			m.image=form.cleaned_data['image']
			m.template=Template.objects.get(userId=request.user,slug=request.POST.get('slug'))
			m.save()
			return HttpResponse(json.dumps({'status':'Image uploaded successfully','url':m.image.url}))
		else:
			print form
			return HttpResponse(json.dumps({'status':'Image uploaded failed'}))
	else: 
		return HttpResponseForbidden('allowed only via POST')

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
					removeSet={'paint-area','paint-area--text','edit-area','edit-area--div','edit-area--text','edit-area--table','selected-area'}
					x.cleanedHtml=cleanHTML(lol,removeSet)
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

def notFound(request):
	return render(request,'yolo/partials/404.html'); 


# def userTemplates(request):
''' For GET request- Currently not used!!! '''
# 	if request.method=='GET':
# 		data=list(Template.objects.filter(userId=request.user).values('slug','name','description'))
# 		print data
# 		return HttpResponse(json.dumps({'templates':data}));

@login_required(login_url='/sign-in')
def editor(request,slug):
	# print os.chdir()
	# fn = os.path.join(settings.PROJECT_ROOT, '../yolo/templates/yolo/editor/mockup.html');
	# mockup = open(fn)
	try:
		t=Template.objects.get(slug=slug,userId=request.user)
	except Template.DoesNotExist:
		return redirect('/notFound')
	if request.method=='POST':
		html=request.POST.dict()['htmlCode']
		t.htmlCode=cleanHTML(html,{'ui-resizable'})
		removeSet={'paint-area','paint-area--text','edit-area','edit-area--div','edit-area--text','edit-area--table','selected-area'}
		x=t.htmlCode
		t.cleanedHtml=cleanHTML(x,removeSet)
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

@login_required(login_url='/sign-in')
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


