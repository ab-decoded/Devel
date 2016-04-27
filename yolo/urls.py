from django.conf.urls import url,handler404
from django.conf import settings
from . import views

# handler404 = 'views.handler404'

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^choose$',views.choose,name="logout"),
	url(r'^insertImage$',views.insertImage,name="insertImage"),
	# url(r'^templates$',views.userTemplates,name="template"),
	url(r'^editor/(?P<slug>[\w-]+)/$',views.editor,name="editor"),	
	url(r'^deleteTemplate/(?P<slug>[\w-]+)/$',views.deleteTemplate,name="deleteTemplate"),	
	url(r'^showcase/(?P<username>\w+)/(?P<slug>[\w-]+)/$',views.showcase,name="editor"),	
	url(r'^downloadAsZip/(?P<username>\w+)/(?P<slug>[\w-]+)/$',views.downloadAsZip,name="downloadAsZip"),	
	# ACCOUNTS
	url(r'^sign-in$',views.signin,name="signin"),
	url(r'^sign-up$',views.signup,name="signup"),
	url(r'^logout$',views.user_logout,name="logout"),
]
