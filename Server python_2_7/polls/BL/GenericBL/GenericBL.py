from ..DAL.mainDAL import geographical_filtering


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