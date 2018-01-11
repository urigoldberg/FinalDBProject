import re

######################################################
########## general validations #######################
######################################################

def sqlInjectionChars(arrOfStrings):
    for s in arrOfStrings:
        if (re.search("[\"\\\/\*\-;']", s)):
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