from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.shortcuts import redirect
from django.shortcuts import render
import os



# cookies stuff

def getCoockieAndResponse(request, pageName, message = "", show = ""):
    cookie = request.COOKIES['user']
    objPath = os.path.join(os.getcwd(),'polls', 'static', pageName)
    obj = open(objPath,'r').read()
    context = Context({"username": cookie, "message": message, "show": show })
    resp = HttpResponse(Template(obj).render(context))
    resp.set_cookie("user",cookie)
    return cookie, resp

def setCoockieAndResponse(pageName, username, message = None):
    resp = redirect(pageName)
    resp.set_cookie("user",username)
    return resp

# sign in stuff
    
def SignInFailed():
    objPath = os.path.join(os.getcwd(),'polls', 'static', "Login.html")
    obj = open(objPath,'r').read()
    context = Context({"message": "What a shit of a username", "show": "true" })
    resp = HttpResponse(Template(obj).render(context))
    return resp

def signNewUser (username, password):
    """Create a new user.
    This function checks if usersTable contains username with the same name.
    If the username available - add it to usersTable and return True, otherwise return False 
    """
    # TBD

    return True

def SignInFailed():
    objPath = os.path.join(os.getcwd(),'polls', 'static', "Login.html")
    obj = open(objPath,'r').read()
    context = Context({"message": "What a shit of a username", "show": "true" })
    resp = HttpResponse(Template(obj).render(context))
    return resp