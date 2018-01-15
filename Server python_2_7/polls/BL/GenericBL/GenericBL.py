from ..DAL.mainDAL import geographical_filtering, yearMostArtistDiedOrBornDB

# return [{"nameOfColumn01":"value01","nameOfColumn02":"value02"....},{},{}]
#in case of error - return None
def generateResFromRes(cols,result):
    res = '[' 
    try:        
        if (cols is None or result is None):
            return None
        for row in result:
            res += '{'
            for col,val in zip(cols,row):
               res += '"' + col + '":"' + val + '",'
            res = res[:len(res)-1] + '},'
        final = res[:len(res)-1] + ']'
        print(final)
        return final
        
    except:
        return None
    

def yearMostArtistDiedOrBorn(dead,num,genre):
    cols,result = yearMostArtistDiedOrBornDB(dead,num,genre)
    return generateResFromRes(cols,result)

    

def get_json_from_generic_request(request):
    return None

def get_json_get_artists(request):
    return None



def get_artists_in_requested_radius(json):
    
    try:
        decoded = json.loads(json)        
        cols,result = geographical_filtering(json)
        if (cols is None or result is None):
            return None
        for row in result:
            res += '{'
            for col,val in zip(cols,row):
               res += '"' + col + '":"' + val + '",'
            res = res[:len(res)-1] + '},'
        final = res[:len(res)-1] + ']}'
        print (final)
        return final

    except (ValueError, KeyError, TypeError):
        print ("JSON format error")
        return None
    
    return final