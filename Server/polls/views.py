from django.shortcuts import render
import os
from polls.GoogleVisionApi.googleVisionSendPost import * 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def mock(request):
    if (request.POST and "photo" in request.POST.keys()):
        return HttpResponse(sendquery(request.POST.get("photo","")))
        #return HttpResponse(request.POST.get("photo",""))
    else:
        return HttpResponse("this is a mock")
	
def mockHTML(request):
    mockHtmlPath = os.path.join(os.getcwd(),'polls', 'mocks', 'htmlphoto.html')
    mockHtml = open(mockHtmlPath,'r').read()
    return HttpResponse(mockHtml)
