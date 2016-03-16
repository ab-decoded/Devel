from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^editor$',views.editor,name="editor"),
	url(r'^sign-in$',views.signin,name="signin"),
	url(r'^sign-up$',views.signup,name="signup"),
	url(r'^logout$',views.user_logout,name="logout"),
]