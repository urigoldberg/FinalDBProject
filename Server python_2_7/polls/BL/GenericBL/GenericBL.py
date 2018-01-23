from ..DAL.mainDAL import geographical_filtering,personalizationDB, yearMostArtistDiedOrBornDB, getColumnValuesDB, youTubeLongestShortestLinkDB, albumsOfGenreWithSalesDB, mostViewedArtistDB, updateYoutubeLinkDB, addLikedSongDB, getUserDetailsDAL, getAllSongsDB

def handleAndInGenre(genre):
#    dicOfKeys = {}
#    dicOfKeys["pictureQuery"] = ["photo"]
#    dicOfKeys["geoService"] = ["longitude","latitude","radius"]
#    dicOfKeys["year"] = ["dead","num","genre"]
#    dicOfKeys["columnname"] = ["column","tablename"]
#    dicOfKeys["youTubeLink"] = ["operation","artistname"]
#    dicOfKeys["SucAlbums"] = ["numOfSales", "genre"]
#    dicOfKeys["mostviewedartist"] = ["location", "genre"]
#    dicOfKeys["updateyoutubelink"] = ["link","song_name","song_artist"]
#    dicOfKeys["add_liked_song"] = ["song_name", "song_artist","user_name"]
#    dicOfKeys["personalization"] = ["user", "bs"]
     if '_AND_' in genre:
         res = genre.replace("_AND_","&")
     return res

def addValuesForFromDic(dic,colum,table,key):
    cols,result = getColumnValuesDB(colum,table)
    op = """<option value="{0}">{0}</option>"""
    value = ""
    if (result != None):
        for row in result:
            value = value + op.format(str(row)[3:-3])
    dic[key] = value
    print("addGenreToDic", value)

def generateResFromRes(cols,result):
#    print ("generateResFromRes - cols",cols, "result",result )
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
    genre = handleAndInGenre(genre)
    if (dead == "0"):
        dead = "year_of_birth"
    else:
        dead = "year_of_death"
    if not (num.isdigit()):
        return None

    cols,result = yearMostArtistDiedOrBornDB(dead,num,genre)
    if (cols == None):
        return '[{"no results were found. you are welcome to try a new query": ""}]'
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
    if (cols == None):
        return '{}'
    return generateResFromRes(cols,result)

def albumsOfGenreWithSales(numOfSales, genre):
    genre = handleAndInGenre(genre)
    if not (numOfSales.isdigit()):
        return None
    cols,result = albumsOfGenreWithSalesDB(numOfSales, genre)
    if (cols == None):
        return '[{"no results were found. you are welcome to try a new query": ""}]'
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
    genre = handleAndInGenre(genre)
    cols,result = mostViewedArtistDB(location, genre)
    if (cols == None):
        return '[{"no results were found. you are welcome to try a new query": ""}]'
    return generateResFromRes(cols,result)

def personalization(param):
    userName = str(param["user"])
    username,password,birth,longness,genre,country = getUserDetailsDAL(userName)
    cols,result = personalizationDB(genre,country,longness)
    if (cols == None):
        return '[{"no results were found. you are welcome to try a new query": ""}]'
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
    song_name,song_artist,user_name = str(param["song_name"]),str(param["song_artist"]), str(param["user_name"])
    res = addLikedSongDB(song_name,song_artist,user_name)
    if(res == True):
        print("finished adding song to liked songs")
        return '"True"'
    else:
        print("else",res)
        if '1062' in res: #meaning it's because of a duplicate
            print("false")
            return '"False"'
        return res

def getAllSongs(param):
    user_name = str(param["user_name"])
    cols,result = getAllSongsDB(user_name)
    if (cols == None):
        return '[{"no results were found. you are free to add songs you like via the Open YouTube or Image to Music queries": ""}]'
    return generateResFromRes(cols,result)

# def get_artists_in_requested_radius(json):

#     try:
#         decoded = json.loads(json)
#         cols,result = geographical_filtering(json)
#         if (cols is None or result is None):
#             return None
#         for row in result:
#             res += '{'
#             for col,val in zip(cols,row):
#                res += '"' + col + '":"' + val + '",'
#             res = res[:len(res)-1] + '},'
#         final = res[:len(res)-1] + ']}'
#         print (final)
#         return final

#     except (ValueError, KeyError, TypeError):
#         print ("JSON format error")
#         return None

#     return final
