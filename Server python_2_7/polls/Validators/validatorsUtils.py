import re
import hashlib

######################################################
########## general validations #######################
######################################################

flownames = []

def basicSec(requests):
    if not (requests.COOKIES.has_key('user') and (requests.COOKIES.has_key('bs'))):
        return False
    h = hashlib.new('ripemd160')
    user = requests.COOKIES['user']
    bs = requests.COOKIES['bs']
    h.update(str(len(user))+user+"basicSec")
    
    return h.hexdigest() == bs
    

def sqlInjectionChars(arrOfStrings):
    for s in arrOfStrings:
        if (re.search("[\"\\\/\*\-;'<>]", s)):
            return False
    return True

def validateLength(arrOfStrings, minLength, maxLength):
    for s in arrOfStrings:
        if (len(s) > maxLength or len(s) < minLength):
            return False
    return True


######################################################
########## signIN \ Login ############################
######################################################

def validateLoginSignIn(request, message):
    # request has un + password
    if not (request.GET and "username" in request.GET and "password" in request.GET):
        message += ["invalid request, please try again"]
        return False
    
    username, password = request.GET["username"], request.GET["password"]
    
    if not validateLength([username,username], 5, 20):
        message += ["username & password must contain at least 5 characters, and not more than 20"]
        return False
    
    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionChars([username,username])):
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
    # request is ..
    if not (request.POST and "flowname" in request.POST.keys() and "params" in request.POST.keys()):
        return False
    
    flowname, params = request.POST["flowname"], request.POST["params"]
    print(params)
    if not validateLength(params, 3, 20):
        return False
    
    if (flowname not in flownames):
        return False
    # request doesn't contain illegal characters - against sql injections
    if not (sqlInjectionChars(params)):
        return False
    
    return True
