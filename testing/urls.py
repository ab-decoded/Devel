from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^abbe$',views.abbe,name="abbe"),
	url(r'^bewde$',views.bewde,name="bewde"),
]