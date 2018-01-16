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
import json as _json

from polls.models import *
from polls.Validators.validatorsUtils import *

from polls.BL.GoogleVisionApiBL.googleVisionSendPost import *
from polls.BL.GoogleVisionApiBL.getSongsByKeywordFromGoogleApi import *
from polls.BL.GeoBL.GeoServiceBL import get_json_from_request, get_artists_in_requested_radius
from polls.BL.GoogleVisionApiBL.googleVisionSendPost import sendGoogleQuery
from polls.BL.GoogleVisionApiBL.getSongsByKeywordFromGoogleApi import get_songs_related_to_keywords
from polls.BL.sqlQueryBuilderBL import queriesBuilder,mockResponse
from polls.BL.GenericBL import GenericBL
from polls.BL.loginManageBL.loginFunctions import *

####################################
############### consts #############
####################################

ERROR_JSON = '{ "isError" : "true", "errorMessage": "An error had occuered", "Results": [] }'


####################################
####### views functions GET ########
####################################

def Login(request):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "Login.html")
    obj = open(objPath,'r').read()
    context = Context({"message": "", "show": "false" })
    resp = HttpResponse(Template(obj).render(context))
    resp.set_cookie("bs","")
    return resp

def default(request):
    return redirect('Login.html')

def UiHomepage(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "UiHomepage.html")
    return resp

def musicExpert(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "musicExpert.html")
    return resp


def filterSongs(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "filterSongs.html")
    return resp

def imageToMusic(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "imageToMusic.html")
    return resp

def searchByKeywords(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "searchByKeywords.html")
    return resp

def searchByGeoLocation(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "searchByGeoLocation.html")
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
        resp = setCookieAndResponse("UiHomepage.html",name )
    else:
        resp = SignInLoginFailed("user or password are incorrect, please try again")
    return resp

@csrf_exempt
def SignInfunc(request):
    # validate
    message = []
    if not (validateLoginSignIn(request,message)):
        return SignInLoginFailed(message[0])
    
    name, password = request.GET['username'],request.GET['password']
    
    # BL
    if (signNewUser(name,password)):
        resp = setCookieAndResponse("UiHomepage.html",name )
    else:
        resp = SignInLoginFailed("user alreay exists")
    return resp

#
#@csrf_exempt
#def pictureService(request):
#    # Validate
#    if not (request.POST and "photo" in request.POST.keys()):
#        return HttpResponse(ERROR_JSON)
#    
#    # Get / Create JSON query
#    json = (sendGoogleQuery(request.POST.get("photo","")))
#    if (json is None):
#        return HttpResponse(ERROR_JSON)
#    
#    #create Json Response
#    responseJson = handleQueryResponse("pictureService",[json])
#    get_songs_related_to_keywords(json)
#        
#    # return to client
#    return HttpResponse(responseJson)
#
#
#@csrf_exempt
#def GeoService(request):
#    # Validate
#    if not (validateGeoService(request)) :
#         return HttpResponse(ERROR_JSON)
#     
#    # Get / Create JSON query
#    json = get_json_from_request(request) #{"longitude": 32,"latitude": 45,"radius": 14}
#    if (json is None):
#        return HttpResponse(ERROR_JSON)
#        
#    #create Json Response
#    responseJson = handleQueryResponse("GeoService",[json])
#        
#    # return to client
#    return HttpResponse(responseJson)



########################################
##### REGULAR QUERY ####################
########################################


@csrf_exempt
def generic(request):
    # Validate
    print ("generic is been called")
    if not (validateGeneric(request)):
         return HttpResponse(ERROR_JSON)
    
    print ("generic passed validation")
     
    # Get / Create JSON query
    json = _json.loads(request.POST["data"])
    flowname, diclist = str(json["flowname"]), json["params"]
    params = {}
    for pair in diclist:
        for key, value in pair.iteritems():
            params[str(key)] = str(value)
    
    print("params",params)
    if (flowname is None or params is None):
        return HttpResponse(ERROR_JSON)
    
    #create Json Response
    responseJson = handleQueryResponse(flowname,params)
        
    # return to client
    print("we return ",responseJson," to flow",flowname)
    return HttpResponse(responseJson)

def handleQueryResponse(flowname,param):
    
    ResultsArray = None
#    print("param in handle query response",param)
    print("flowname is",flowname)
    #check flow name
    if (flowname == "pictureQuery"):
        print("sending picture to google")
        json = (sendGoogleQuery(param['photo']))
        print("sent picture to google")
        ResultsArray = get_songs_related_to_keywords(json)
    
    if (flowname == "GeoService"):
        ResultsArray = get_artists_in_requested_radius(param)
        
    if (flowname == "Filterkeys"):
        ResultsArray = None
        
    if (flowname == "year"):
        dead, num, genre = str(param["dead"]),str(param["num"]),str(param["genre"])
        if (dead == "0"):
            dead = "year_of_birth"
        else:
            dead = "year_of_death"
        if (num.isdigit()):
            ResultsArray = GenericBL.yearMostArtistDiedOrBorn(dead,num,genre)
    # more ifs..
    
    # If ResultsArray == None, an error has occuered
    # Otherwise, the function returned array for json
    if (ResultsArray == None):
        return ERROR_JSON
    
    return '{ "isError" : "false", "errorMessage": "", "Results": ' + ResultsArray + '}' 
    



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





