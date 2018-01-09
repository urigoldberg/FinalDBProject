# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from polls.GoogleVisionApi.googleVisionSendPost import *
from polls.sqlQueryBuilder import queriesBuilder,mockResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.shortcuts import redirect
from django.shortcuts import render
from polls.models import *
import MySQLdb
import os





#def book_list(request):
#    db = MySQLdb.connect(user='me', db='mydb',  passwd='secret', host='localhost')
#    cursor = db.cursor()
#    cursor.execute('SELECT name FROM books ORDER BY name')
#    names = [row[0] for row in cursor.fetchall()]
#    db.close()
#    return render(request, 'book_list.html', {'names': names})

# pages:

def default(request):
    return redirect('UiHomepage.html')

def UiHomepage(requests):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "UiHomepage.html")
    obj = open(objPath,'r').read()
    return HttpResponse(obj)

def imageToMusic(requests):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "imageToMusic.html")
    obj = open(objPath,'r').read()
    return HttpResponse(obj)

def searchByKeywords(requests):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "searchByKeywords.html")
    obj = open(objPath,'r').read()
    return HttpResponse(obj)

def searchByGeoLocation(requests):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "searchByGeoLocation.html")
    obj = open(objPath,'r').read()
    return HttpResponse(obj)



# services
@csrf_exempt
def pictureService(request):
    
    #get query
    if (request.POST and "photo" in request.POST.keys()):
        json = (sendGoogleQuery(request.POST.get("photo","")))
        # parse json to string array
        # build query
        # build respones
        #return response
        return HttpResponse(mockResponse.mockResponse)
        
    #Path = os.path.join(os.getcwd(),'polls', 'Client', 'htmlphoto.html')
    return HttpResponse(str(request))






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
    for artist in Artists.objects.raw('SELECT ID FROM DbMysql12.Artists where ID = 0;'):
        print(artist.id)
#    db = MySQLdb.connect(user='DbMysql12', db='DbMysql12',  passwd='DbMysql12', host='localhost', port = 3305)
#    cursor = db.cursor()
#    cursor.execute('SELECT title FROM DbMySql12.Seed;')
#    names = [row[0] for row in cursor.fetchall()]
#    print(names)
#    print(cursor.description)
#    db.close()
#    c = connections['DbMysql12'].cursor()
#    c.execute("SELECT title FROM DbMySql12.Seed;")
#    rows = c.fetchall()
    return HttpResponse(str(artist))
    
    
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





