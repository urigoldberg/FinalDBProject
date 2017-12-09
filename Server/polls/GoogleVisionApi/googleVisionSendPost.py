try:
        import requests
except ImportError:
        import pip
        pip.main(['install', 'requests'])
        import requests
# create JSON FILE. uses mock for no
def sendquery(pic):
    data = """{
  "requests": [
    {
      "image": {
        "content": """+'"'+pic+'"'+"""
       },
       "features": [
          {
            "type": "LOGO_DETECTION",
            "maxResults": "10"
          },
          {
            "type": "LABEL_DETECTION",
             "maxResults": "10"
          },
          {
            "type": "TEXT_DETECTION",
            "maxResults": "10"
          }
       ]
     }
  ]
}"""
    #data = open('/Users/<username>/testdata/vision.json', 'rb').read()

    ########## API KEY MAY COST MONEY AND IS LIMITED ############
    ########## DO NOT EXPOSE IT #################################
    APIKEY = "AIzaSyB5gD9fZjNN0pdXWNAVbyJo4Cqamoje7hk"
    #############################################################
    response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key='+APIKEY,
        data=data,    headers={'Content-Type': 'application/json'})
    return (response.text)
