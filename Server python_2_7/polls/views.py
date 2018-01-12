# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.shortcuts import redirect
from django.shortcuts import render

import MySQLdb
import os

from polls.models import *
from polls.Validators.validatorsUtils import *

from polls.BL.GoogleVisionApiBL.googleVisionSendPost import *
from polls.BL.GoogleVisionApiBL.getSongsByKeywordFromGoogleApi import *
from polls.BL.sqlQueryBuilderBL import queriesBuilder,mockResponse
from polls.BL.loginManageBL.loginFunctions import *


####################################
####### views functions GET ########
####################################

def Login(request):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "Login.html")
    obj = open(objPath,'r').read()
    context = Context({"message": "", "show": "false" })
    resp = HttpResponse(Template(obj).render(context))
    return resp

def default(request):
    return redirect('Login.html')

def UiHomepage(requests):
    if not requests.COOKIES.has_key('user' ):
        return redirect('Login.html')
    user, resp = getCoockieAndResponse(requests, "UiHomepage.html")
    return resp

def imageToMusic(requests):
    if not requests.COOKIES.has_key('user' ):
        return redirect('Login.html')
    user, resp = getCoockieAndResponse(requests, "imageToMusic.html")
    return resp

def searchByKeywords(requests):
    if not requests.COOKIES.has_key('user' ):
        return redirect('Login.html')
    user, resp = getCoockieAndResponse(requests, "searchByKeywords.html")
    return resp

def searchByGeoLocation(requests):
    if not requests.COOKIES.has_key('user' ):
        return redirect('Login.html')
    user, resp = getCoockieAndResponse(requests, "searchByGeoLocation.html")
    return resp



####################################
####### views functions POST #######
####################################
    
@csrf_exempt
def LoginUserfunc(request):
    
    # validate
    message = []
    if not (validateLoginSignIn(request,message)):
        return SignInLoginFailed(message[0])
    
    name, password = request.GET['username'],request.GET['password']

    # BL
    if (loginUser(name,password)):
        resp = setCoockieAndResponse("UiHomepage.html",name )
    else:
        resp = SignInLoginFailed("user or password are incorrect, please try again")
    return resp

@csrf_exempt
def SignInfunc(request):
    # validate
    message = []
    if not (validateLoginSignIn(request,message)):
        return SignInFailed(message[0])
    
    name, password = request.GET['username'],request.GET['password']
    
    # BL
    if (signNewUser(name,password)):
        resp = setCoockieAndResponse("UiHomepage.html",name )
    else:
        resp = SignInLoginFailed("user alreay exists")
    return resp


@csrf_exempt
def pictureService(request):
    #get query
    if (request.POST and "photo" in request.POST.keys()):
        json = (sendGoogleQuery(request.POST.get("photo","")))
        responseJson = get_songs_related_to_keywords(json)
        return HttpResponse(responseJson)
        
    return HttpResponse(None)

@csrf_exempt
def GeoService(request):
    #get query
    if (request.POST and "geo" in request.POST.keys()):
        json = (sendGoogleQuery(request.POST.get("photo","")))
        responseJson = get_songs_related_to_keywords(json)
        return HttpResponse(responseJson)
        
    return HttpResponse(None)






#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
#def main(request):
#    page = "UiHomepage.html"
#    objPath = os.path.join(os.getcwd(),'polls', 'static', page)
#    obj = open(objPath,'r').read()
##    print(request.META['PATH_INFO'])
##    #print ( request.META['PATH_INFO'] + "\n" + request.META['QUERY_STRING'])
##    if  not (request.META['QUERY_STRING'] == ""):
##        page = request.META['QUERY_STRING'].replace("\\main\\")
##        print(page)
##    objPath = os.path.join(os.getcwd(),'polls', 'static', page)
##    obj = open(objPath,'r').read()
#    return HttpResponse(obj)
#
#        
        
#        
#    print(request.build_absolute_uri())
#    print(request.build_absolute_uri('/')[:-1].strip("/"))
#    print ( request.META['PATH_INFO'] + "\n" + request.META['QUERY_STRING'])



def test(request):
#    for artist in Artists.objects.raw('SELECT ID FROM DbMysql12.Artists where ID = 0;'):
#        print(artist.id)
    db = MySQLdb.connect(user='DbMysql12', db='DbMysql12',  passwd='DbMysql12', host='localhost', port = 3305)
    cursor = db.cursor()
    a = cursor.execute('SELECTs * FROM users_table LIMIT 3;')
    print ("a is " + str(a))
    #print(cursor.execute("""insert into DbMysql12.users_table values ('urig','shcdshory');"""))
    #names = [row[0] for row in cursor.fetchall()]
    #print(names)
    #db.commit()
    print(cursor.fetchall())
    print(cursor.description)
    db.close()
#    c = connections['DbMysql12'].cursor()
#    c.execute("SELECT title FROM DbMySql12.Seed;")
#    rows = c.fetchall()
    return HttpResponse(str("asa"))
    
    
@csrf_exempt
def mockHTML(request):
    if request.method == 'GET':
        mockHtmlPath = os.path.join(os.getcwd(),'polls', 'mocks', 'htmlphoto.html')
        mockHtml = open(mockHtmlPath,'r').read()
        return HttpResponse(mockHtml)
    else:
        if (request.POST and "photo" in request.POST.keys()):
            return HttpResponse(sendGoogleQuery(request.POST.get("photo","")))
            #return HttpResponse(request.POST.get("photo",""))
        else:
            return HttpResponse("this is a mock")





