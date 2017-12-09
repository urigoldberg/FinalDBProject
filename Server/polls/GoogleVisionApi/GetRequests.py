import urllib.request
def getToText(url):
    return urllib.request.urlopen(r"https://api.lyrics.ovh/v1/Coldplay/Adventure%20of%20a%20Lifetime").read()
