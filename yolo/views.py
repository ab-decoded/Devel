from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request,'yolo/index.html')

def editor(request):
	return render(request,'yolo/editor/editor.html')
