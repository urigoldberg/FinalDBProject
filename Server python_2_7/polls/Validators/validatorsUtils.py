import re
import hashlib
import json as _json

from ..BL.GenericBL.GenericBL import getDicOfParams

######################################################
########## general validations #######################
######################################################


def basicSec(requests):
    if not (requests.COOKIES.has_key('user') and (requests.COOKIES.has_key('bs'))):
        return False
    h = hashlib.new('ripemd160')
    user = requests.COOKIES['user']
    bs = requests.COOKIES['bs']
    h.update(str(len(user))+user+"basicSec")
    
    return h.hexdigest() == bs
    

def sqlInjectionChars(dic):
    
    for key, value in dic.iteritems():
        if (re.search("[\"\*#;'<>]", value)):
            return False
    return True

def sqlInjectionCharsList(lst):
    
    for  value in lst:
        if (re.search("[\"\\\/\*#;'<>]", value)):
            return False
    return True

def validateLength(dic, minLength, maxLength):
    for key, value in dic.iteritems():
        if (len(value) > maxLength or len(value) < minLength):
            return False
    return True

def validateLengthList(lst, minLength, maxLength):
    for  value in lst:
        if (len(value) > maxLength or len(value) < minLength):
            return False
    return True

def hasKeys(flow,dic):
    dicOfKeys = {}
    dicOfKeys["pictureQuery"] = ["photo"]
    dicOfKeys["geoService"] = ["longitude","latitude","radius"]
    dicOfKeys["year"] = ["dead","num","genre"]
    dicOfKeys["columnname"] = ["column","tablename"]
    dicOfKeys["youTubeLink"] = ["operation","artistname"]
    dicOfKeys["SucAlbums"] = ["numOfSales", "genre"]
    dicOfKeys["mostviewedartist"] = ["location", "genre"]
    dicOfKeys["updateyoutubelink"] = ["link","song_name","song_artist"]
    dicOfKeys["add_liked_song"] = ["song_name", "song_artist","user_name"]
    dicOfKeys["personalization"] = ["user", "bs"]
    dicOfKeys["get_all_songs"] = ["user_name"]
    keys = [str(key) for key, value in dic.iteritems()]
    print("keys",keys)
    print("dicOfKeys[flow]",dicOfKeys[flow])
    # is subset
    return set(keys) == set(dicOfKeys[flow])

######################################################
########## signIN \ Login ############################
######################################################

def validateSignIn(request, message):
    # request has un + password
    if not (request.GET and "username" in request.GET and "password" in request.GET and 'datebith' in request.GET and 'yesNo' in request.GET and 'genre' in request.GET and 'Country' in request.GET):
        message += ["invalid request, please try again"]
        return False
    
    username, password,datebith,yesNo,genre,Country = request.GET['username'],request.GET['password'],request.GET['datebith'],request.GET['yesNo'],request.GET['genre'],request.GET['Country']
    
    if not validateLengthList([username,password], 5, 20):
        message += ["username & password must contain at least 5 characters, and not more than 20"]
        return False
    
    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionCharsList([username,password,datebith,yesNo,genre,Country])):
        message += ["invalid request, please try again"]
        return False
    
    return True


def validateLogin(request, message):
    # request has un + password
    if not (request.GET and "username" in request.GET and "password"):
        message += ["invalid request, please try again"]
        return False
    
    username, password= request.GET['username'],request.GET['password']
    
    if not validateLengthList([username,password], 5, 20):
        message += ["username & password must contain at least 5 characters, and not more than 20"]
        return False
    
    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionCharsList([username,password])):
        message += ["invalid request, please try again"]
        return False
    
    return True

######################################################
##################### Geo ############################
######################################################

def validateGeoService(request):
    # request has un + password
    if not (request.POST and "geo" in request.POST.keys()):
        return False
    
    if not validateLength([username,username], 5, 20):
        return False
    
    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionChars([username,username])):
        return False
    
    return True



def validateGeneric(request):
    print("start validating")
       
    
    flownames = ["pictureQuery", "geoService", "year","columnname","youTubeLink","SucAlbums"\
                 ,"mostviewedartist", "updateyoutubelink","add_liked_song","personalization","get_all_songs"]
    
    # request is ..
    if not (request.POST and "data" in request.POST.keys()):
        print("donsnt have data =")
        return False
    
    json = None
    try:
        json = _json.loads(request.POST["data"])
    except ValueError:
        print("invalid json")
        return False
    
    if (type(json["params"]) is not list or len(json["params"]) == 0):
        print("params is not good")
        return False

    flowname, diclist = str(json["flowname"]), json["params"]
     # Get params dis
    if (flowname == "filterKeys"):
        params = getDicOfParams(diclist,True)
    else:
        params = getDicOfParams(diclist,False)
    
    if (flowname not in flownames):
        print("flowname not in flownames")
        return False
    
    # param is a dic contains lists
    if not (flowname == "filterKeys"):
        if not (hasKeys(flowname, params)):
            print("keys are not updated")
            return False
    # param values are lists, check each one seperatelly
    else:
        for key, value in params.iteritems():
            if not (sqlInjectionCharsList (value)):
                return False
    

    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionChars(params)):
        print("sqlInjectionChars")
        return False
    
    # speaciel validators:
    
    return True
