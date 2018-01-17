from ..DAL.mainDAL import geographical_filtering,personalizationDB, yearMostArtistDiedOrBornDB, getColumnValuesDB, youTubeLongestShortestLinkDB, albumsOfGenreWithSalesDB, mostViewedArtistDB, updateYoutubeLinkDB, addLikedSongDB, getUserDetailsDAL, getAllSongsDB

def addValuesForFromDic(dic,colum,table,key):
    cols,result = getColumnValuesDB(colum,table)
    op = """<option value="{0}">{0}</option>"""
    value = ""
    for row in result:
        value = value + op.format(str(row)[3:-3])
    dic[key] = value
    print("addGenreToDic", value)

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
    if (dead == "0"):
        dead = "year_of_birth"
    else:
        dead = "year_of_death"
    if not (num.isdigit()):
        return None
    
    cols,result = yearMostArtistDiedOrBornDB(dead,num,genre)
    return generateResFromRes(cols,result)

def getColumnValues(column, tablename):
    cols,result = getColumnValuesDB(column, tablename)
    return generateResFromRes(cols,result)

def youTubeLongestShortestLink(name,op):
    if (op == "min"):
        op = "<"
    else:
        op = ">"
    cols,result = youTubeLongestShortestLinkDB(name,op)
    return generateResFromRes(cols,result)

def albumsOfGenreWithSales(numOfSales, genre):
    if not (numOfSales.isdigit()):
        return None
    cols,result = albumsOfGenreWithSalesDB(numOfSales, genre)
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
    
def mostViewedArtist(param):
    location, genre = str(param["location"]),str(param["genre"])
    cols,result = mostViewedArtistDB(location, genre)
    return generateResFromRes(cols,result)

def personalization(param):
    userName = str(param["user"])
    username,password,birth,longness,genre,country = getUserDetailsDAL(userName)
    cols,result = personalizationDB(genre,country,longness)
    return generateResFromRes(cols,result)

def validate_link(link):
    import urllib2
    if "youtube.com" not in link: 
        return False
    try:
        urllib2.urlopen(link)
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False
    return True

def updateYoutubeLink(param):
    link,song_name,song_artist = str(param["link"]), str(param["song_name"]),str(param["song_artist"])
    if(validate_link(link)):
        return updateYoutubeLinkDB(link,song_name,song_artist)
    else:
        return None
    

def addLikedSong(param):
    print("at addLikedSong")
    song_name,song_artist,user_name = str(param["song_name"]),str(param["song_artist"]), str(param["user_name"])
    if(addLikedSongDB(song_name,song_artist,user_name)):
        print("finished adding song to liked songs")
        return "True"
    else:
        return None

def getAllSongs(param):
    user_name = str(param["user_name"])
    cols,result = getAllSongsDB(user_name)
    return generateResFromRes(cols,result)

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
