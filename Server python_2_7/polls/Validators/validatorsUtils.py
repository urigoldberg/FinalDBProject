import re
import hashlib
import json as _json

from ..BL import GenericBL

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
        if (re.search("[\"\\\/\*#;'<>]", value)):
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
    dicOfKeys["geoService"] = ["shit"]
    dicOfKeys["year"] = ["dead","num","genre"]
    dicOfKeys["columnname"] = ["column","tablename"]
    dicOfKeys["youTubeLink"] = ["operation","artistname"]
    
    keys = [str(key) for key, value in dic.iteritems()]
    print(keys)
    print(dicOfKeys[flow])
    # is subset
    return set(keys) == set(dicOfKeys[flow])

######################################################
########## signIN \ Login ############################
######################################################

def validateLoginSignIn(request, message):
    # request has un + password
    if not (request.GET and "username" in request.GET and "password" in request.GET):
        message += ["invalid request, please try again"]
        return False
    
    username, password = request.GET["username"], request.GET["password"]
    
    if not validateLengthList([username,username], 5, 20):
        message += ["username & password must contain at least 5 characters, and not more than 20"]
        return False
    
    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionCharsList([username,username])):
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
    
    flownames = ["pictureQuery", "geoService", "year","columnname","youTubeLink"]
    
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
        params = GenericBL.getDicOfParams(diclist,True)
    else:
        params = GenericBL.getDicOfParams(diclist,False)
    
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
    
#    if not validateLength(params, 1, 20):
#        print("to short")
#        return False
    

    # request doesn't contain illegal characters - against sql injections
    if(flowname != "pictureQuery"):
        if not (sqlInjectionChars(params)):
            print("sqlInjectionChars")
            return False
    
    # speaciel validators:
    
    return True
