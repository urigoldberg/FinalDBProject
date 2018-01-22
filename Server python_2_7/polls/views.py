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
from polls.BL.GeoBL.GeoServiceBL import get_artists_in_requested_radius
from polls.BL.GoogleVisionApiBL.googleVisionSendPost import sendGoogleQuery
from polls.BL.GoogleVisionApiBL.getSongsByKeywordFromGoogleApi import get_songs_related_to_keywords
from polls.BL.sqlQueryBuilderBL import queriesBuilder,mockResponse
from polls.BL.GenericBL import GenericBL
from polls.BL.loginManageBL.loginFunctions import *

####################################
############### consts #############
####################################

ERROR_JSON = '{ "isError" : "true", "errorMessage": "An error had occurred", "Results": [] }'


####################################
####### views functions GET ########
####################################

def Login(request):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "Login.html")
    obj = open(objPath,'r').read()
    dic = {"message": "", "show": "false" }
    context = Context(dic)
    
    # replace for form values, which came from db
    GenericBL.addValuesForFromDic(dic,"genre", "artists","allGenre")
    GenericBL.addValuesForFromDic(dic,"name", "CountryArtists","allCountries")
    obj = obj.replace("{{allGenre}}",dic["allGenre"]).replace("{{allCountries}}",dic["allCountries"])

    
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

def PersonalQueries(requests):
    if not basicSec(requests):
        return redirect('Login.html')
    user, resp = getCookieAndResponse(requests, "PersonalQueries.html")
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
    if not (validateLogin(request,message)):
        return SignInLoginFailed(message[0])
    
    name, password = request.GET['username'],request.GET['password']
    # BL
    if (loginUser(name,password,)):
        resp = setCookieAndResponse("UiHomepage.html",name )
    else:
        resp = SignInLoginFailed("user or password are incorrect, please try again")
    return resp

@csrf_exempt
def SignInfunc(request):
    # validate
    message = []
    if not (validateSignIn(request,message)):
        return redirect('Login.html')
        #return SignInLoginFailed(message[0])
    
    name, password,datebith,yesNo,genre,Country = request.GET['username'],request.GET['password'],request.GET['datebith'],request.GET['yesNo'],request.GET['genre'],request.GET['Country']
    
    # BL
    if (signNewUser(name, password,datebith,yesNo,genre,Country)):
        resp = setCookieAndResponse("UiHomepage.html",name )
    else:
        return redirect('Login.html')
    #resp = SignInLoginFailed("user alreay exists")
    return resp



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
    
    # Get params dis
    if (flowname == "filterKeys"):
        params = GenericBL.getDicOfParams(diclist,True)
    else:
        params = GenericBL.getDicOfParams(diclist,False)

#    print("params",params)
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
    
    if (flowname == "geoService"):
        print("in flow geoservice, param is %s" % param)
        ResultsArray = get_artists_in_requested_radius(param)
        
    if (flowname == "Filterkeys"):
        ResultsArray = None
        
    if (flowname == "year"):
        dead, num, genre = str(param["dead"]),str(param["num"]),str(param["genre"])
        ResultsArray = GenericBL.yearMostArtistDiedOrBorn(dead,num,genre)
            
    if (flowname == "columnname"):
        column, tablename = str(param["column"]),str(param["tablename"])
        ResultsArray = GenericBL.getColumnValues(column, tablename)
        
    if (flowname == "youTubeLink"):
        op, artistname = str(param["operation"]),str(param["artistname"])
        ResultsArray = GenericBL.youTubeLongestShortestLink(artistname,op)
        
    if (flowname == "SucAlbums"):
        numOfSales, genre = str(param["numOfSales"]),str(param["genre"])
        ResultsArray = GenericBL.albumsOfGenreWithSales(numOfSales, genre)
     
    if (flowname == "mostviewedartist"):
        ResultsArray = GenericBL.mostViewedArtist(param)
        
    if (flowname == "updateyoutubelink"):
        ResultsArray = GenericBL.updateYoutubeLink(param)
    
    if (flowname == "add_liked_song"):
        ResultsArray = GenericBL.addLikedSong(param)
        
    if (flowname == "personalization"):
        ResultsArray = GenericBL.personalization(param)
        
    if (flowname == "get_all_songs"):
        ResultsArray = GenericBL.getAllSongs(param)
    
    # If ResultsArray == None, an error has occuered
    # Otherwise, the function returned array for json
    if (ResultsArray == None):
        return ERROR_JSON
    
    
    
    return '{ "isError" : "false", "errorMessage": "", "Results": ' + ResultsArray + '}' 
 
   
