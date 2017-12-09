# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from polls.GoogleVisionApi.googleVisionSendPost import *
from django.views.decorators.csrf import csrf_exempt
import os


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index1(request):
    return HttpResponse("fdgdsgffdsg")

@csrf_exempt
def mockHTML(request):
    if request.method == 'GET':
        mockHtmlPath = os.path.join(os.getcwd(),'polls', 'mocks', 'htmlphoto.html')
        mockHtml = open(mockHtmlPath,'r').read()
        return HttpResponse(mockHtml)
    else:
        if (request.POST and "photo" in request.POST.keys()):
            return HttpResponse(sendquery(request.POST.get("photo","")))
            #return HttpResponse(request.POST.get("photo",""))
        else:
            return HttpResponse("this is a mock")
