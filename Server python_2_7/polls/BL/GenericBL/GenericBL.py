from ..DAL.mainDAL import geographical_filtering, yearMostArtistDiedOrBornDB, getColumnValuesDB

# return [{"nameOfColumn01":"value01","nameOfColumn02":"value02"....},{},{}]
#in case of error - return None
def generateResFromRes(cols,result):
    print ("generateResFromRes - cols",cols, "result",result )
    res = '[' 
    try:        
        if (cols is None or result is None):
            return None
        for row in result:
            res += '{'
            for col,val in zip(cols,row):
               res += '"' + str(col) + '":"' + str(val) + '",'
            res = res[:len(res)-1] + '},'
        final = res[:len(res)-1] + ']'
        print(final)
        return final
        
    except Exception as e:
        print (e.message)
        return None
    

def yearMostArtistDiedOrBorn(dead,num,genre):
    cols,result = yearMostArtistDiedOrBornDB(dead,num,genre)
    return generateResFromRes(cols,result)

def getColumnValues(column, tablename):
    cols,result = getColumnValuesDB(column, tablename)
    return generateResFromRes(cols,result)
    
########### GENERAL UTILS ##############
def getDicOfParams(diclist, isUnique):
    try:
        params = {}
        # unique keys in dic
        if (isUnique):
            for pair in diclist:
                for key, value in pair.iteritems():
                    if (str(key) in params):
                        params[str(key)] += [str(value)]
                    else:
                        params[str(key)] = [str(value)]
        # not unique keys in dic
        else:
            for pair in diclist:
                for key, value in pair.iteritems():
                    params[str(key)] = str(value)
        return params
    except Exception as e:
        print ("getDicOfParams errore ",e.message)
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