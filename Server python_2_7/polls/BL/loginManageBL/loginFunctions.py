from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.shortcuts import redirect
from django.shortcuts import render
import hashlib
from ..DAL.mainDAL import *
import os



# cookies stuff

def getCoockieAndResponse(request, pageName, message = "", show = ""):
    user = request.COOKIES['user']
    objPath = os.path.join(os.getcwd(),'polls', 'static', pageName)
    obj = open(objPath,'r').read()
    context = Context({"username": user, "message": message, "show": show })
    resp = HttpResponse(Template(obj).render(context))
    return user, resp

def setCoockieAndResponse(pageName, username, message = None):
    '''Set cookie contains username, in order to present it in some
    pages and get details about him/her from usersTable if necessary'''
    resp = redirect(pageName)
    resp.set_cookie("user",username)
    
    #calculate hash
    h = hashlib.new('ripemd160')
    h.update(username+"basicSec")
    resp.set_cookie("bs",h.hexdigest())
    return resp

# sign in stuff

def signNewUser (username, password):
    """Create a new user.
    This function checks if usersTable contains username with the same name.
    If the username available - add it to usersTable and return True, otherwise return False 
    """
    if (addNewUserDAL(username,password)):
        return True
    return False


def loginUser (username, password):
    correctPassword = getUserPasswordUsernameDAL(username)
    return correctPassword == password
    

def SignInLoginFailed(message):
    objPath = os.path.join(os.getcwd(),'polls', 'static', "Login.html")
    obj = open(objPath,'r').read()
    context = Context({"message": message, "show": "true" })
    resp = HttpResponse(Template(obj).render(context))
    return resp
