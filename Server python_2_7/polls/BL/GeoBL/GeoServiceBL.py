from ..DAL.mainDAL import geographical_filtering
def get_json_from_request(request):
    pass


def get_artists_in_requested_radius(json):
    

    try:
        decoded = json.loads(json)
#        #get all keywords
#        cnt = 0
#        for x in decoded['labelAnnotations']:
##            print (x['description'])
#            cnt += 1
#            if (cnt == 5): 
#                break
        #keyword = str(decoded['responses'][0]['labelAnnotations'][0]['description'])
        
        result = geographical_filtering(json)
        
        keywords = list(OrderedDict.fromkeys(array))[:5]
        rows = googleApiSearchSongsByKeyWord(keywords)
        
        
    except (ValueError, KeyError, TypeError):
        print ("JSON format error")
    
    return rows