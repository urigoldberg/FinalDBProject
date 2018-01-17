import MySQLdb
import os
import string

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

######CLASS###########

class DBconnection():
    configPath = os.path.join(os.getcwd(),'polls', 'BL', "DAL","config")
    config = open(configPath,"r").read()
    details = config.split("\n")
    cursor = None
    _user = details[0].split(":")[1]
    _db = details[1].split(":")[1]
    _passwd = details[2].split(":")[1]
    _host = details[3].split(":")[1]
    _port = int(details[4].split(":")[1])
    _succ = False
    _results = None
    _rowsReturned = -1
    _exception = None
    _open = False
    _columns = None
    printable = set(string.printable)
    
    
    

    
    def connect(self):
        if not (self._open):
            self._db = MySQLdb.connect(user=self._user, db=self._db,  passwd=self._passwd, host=self._host, port = self._port, charset='utf8',use_unicode=True)
            self.cursor = self._db.cursor()
            self._open = True
            
    def doSelectQuery(self, query):
        
        self.connect()
        
        # prepare
        self._succ = False
        self._rowsReturned = -1
        self._results = None
        self._exception = None
        
        # succed
        try:
            self._rowsReturned = self.cursor.execute(query)
            print("executed successfully. num of rows returned",self._rowsReturned)
            self._succ = True
            self._results = self.cursor.fetchall()
            print("done fetching results, description is", self.cursor.description)
            if(self._rowsReturned > 0):
                self._columns = [str(i[0]) for i in self.cursor.description]
            print("columns are",self._columns)
            return True
        
        # fail
        except Exception as e:
            self._exception = (e.message)
            print("exception has occurred in doSelectQuery")
            return False
        
    def doQuery(self, query):  
        #this is used for DB
        self.connect()
        
        # prepare
        self._succ = False
        self._rowsReturned = -1
        self._results = None
        self._exception = None
        
        # succed
        try:
            self._rowsReturned = self.cursor.execute(query)
            self._db.commit()
            self._succ = True
            return True
        
        # fail
        except Exception as e:
            self._exception = (e.message)
            print("exception has occurred in doQuery")
            return False
        
        
        
    def insertQuery(self, query):
        
        self.connect()
        
        # prepare
        self._succ = False
        self._rowsReturned = -1
        self._results = None
        self._exception = None
        
        # succed
        try:
            self._rowsReturned = self.cursor.execute(query)
            self._db.commit()
            self._succ = True
            return True
        
        # fail
        except Exception as e:
            self._exception = (e.message)
            return False
    
    def close(self):
        if (self._open):
            self._db.close()
            self._open = False
        
    
        
#############LOGIN######################
    
def addNewUserDAL(name, password,datebith,yesNo,genre,Country):
    
    query = """insert into DbMysql12.users_table values ('{0}','{1}','{2}','{3}','{4}','{5}');""".format(name, password,datebith,yesNo,genre,Country)
    con = DBconnection()
    print("addNewUserDAL", query)
    if (con.insertQuery(query)):
        con.close()
        return True
    
    con.close()
    return False


def getUserPasswordUsernameDAL(username):
    query = "select password from DbMysql12.users_table where user_name = '"+username+"';";
    con = DBconnection()
    if (con.doSelectQuery(query) and con._rowsReturned == 1):
        con.close()
        return con._results[0][0]
    return None

def getUserDetailsDAL(username):
    query = "select * from DbMysql12.users_table where user_name = '"+username+"';";
    con = DBconnection()
    if (con.doSelectQuery(query) and con._rowsReturned == 1):
        con.close()
        return con._results[0]
    return None
 

    

###########GOOGLE API####################
    
def googleApiSearchSongsByKeyWord(keywords):
    if len(keywords) == 0:
        return None
    keywords_for_full_text = ""
    for keyword in keywords:
        keywords_for_full_text += ' +'+ str(keyword)
    create_search_table_query = """
    drop table if exists DbMysql12.temp_keywords;
    create table DbMysql12.temp_keywords(
	song_id int,
    lyrics text
);

Insert Into DbMysql12.temp_keywords
SELECT lyr.song_id ,lyr.lyrics FROM DbMysql12.Lyrics lyr
where match(lyr.lyrics) against ('"""+keywords_for_full_text+"""' in natural language mode);
    """
    
    con = DBconnection()
    con.doQuery(create_search_table_query)
    con.close()
    print("finished creating table")
    query = "select t.keyword as 'Keyword',t.title as 'Song Name',t.name as 'Artist Name',t.media_url as 'Youtube Link' from ("
    for index,keyword in enumerate(keywords):
        if not index == 0:
            query += "union all "
        numOfAppear = 5 - index + 1
        # TO DO - DUPLICATED ROWS
        query += """select * from
        (SELECT 
 inner_songs.title, art.name,
 inner_songs.num_occurrences, inner_songs.media_url, '"""+str(keyword)+"""' as keyword
FROM (SELECT * FROM
(SELECT song_id,
((LENGTH(lyrics) - LENGTH(REPLACE(lyrics, '"""+str(keyword)+"""', '')))
/ LENGTH('"""+str(keyword)+"""'))
AS num_occurrences FROM
DbMysql12.temp_keywords) lyr
INNER JOIN DbMysql12.Song son ON lyr.song_id = son.id)  inner_songs
INNER JOIN
DbMysql12.artists art ON art.db_id = inner_songs.artist_db_id
ORDER BY num_occurrences DESC
LIMIT """+str(numOfAppear) +""") as tbl"""+str(index) +""" 
"""
    con = DBconnection()
    query += """) t where t.num_occurrences > 0 order by t.num_occurrences desc;
"""
    
    if (con.doSelectQuery(query)):
        print("finished googleAPI successfuly")
        con.close()   
        return con._columns, con._results 
    return None

###########Geographical####################
def geographical_filtering(longitude, latitude, radius):
    query = """SELECT DISTINCT a.name FROM DbMysql12.CountryArtists AS ca
    INNER JOIN DbMysql12.artists AS a ON ca.artist_id=a.id
    WHERE lower(ca.name) IN
    (SELECT lower(DbMysql12.Country.name) FROM DbMysql12.Country
    WHERE
     (111.111 *
    DEGREES(ACOS(COS(RADIANS(Country.latitude))
         * COS(RADIANS({1}))
         * COS(RADIANS(Country.longitude - {0}))
         + SIN(RADIANS(Country.latitude))
         * SIN(RADIANS({1})))) )< {2});""".format(longitude, latitude, radius)

    con = DBconnection()
    if (con.doSelectQuery(query)):
        con.close()
        return con._columns,con._results
    return None,None

###########maigc years####################
def yearMostArtistDiedOrBornDB(dead,num,genre):
    query = """SELECT 
    t.genre, t.{0}, COUNT(t.genre) AS numOfArts
FROM
    DbMysql12.artists t
WHERE
    t.{0} IS NOT NULL
    AND t.genre = '{2}'
        AND t.genre IS NOT NULL
        AND t.genre NOT LIKE ''
GROUP BY t.genre
HAVING numOfArts > {1}
ORDER BY numOfArts DESC;""".format(dead,num,genre)
    print("query",query)
    con = DBconnection()
    if (con.doSelectQuery(query)):
        con.close()
        return con._columns,con._results
    return None,None

##########Get column values#####################
def getColumnValuesDB(column, tablename):
    query = """SELECT DISTINCT
    t.{0}
FROM
    DbMysql12.{1} t
WHERE
    t.{0} IS NOT NULL
        AND t.{0} NOT LIKE '';""".format(column, tablename)
    print("query",query)
    con = DBconnection()
    if (con.doSelectQuery(query) and con._rowsReturned > 0):
        con.close()
        return con._columns,con._results
    return None,None

##########Get youtuble link of artist################
def youTubeLongestShortestLinkDB(name,op):
    query = """SELECT 
    a.title as song_name, b.name as artist_name, a.media_url as URL 
FROM
    DbMysql12.Song a,
    DbMysql12.artists b
WHERE
    a.artist_id = b.id
        AND b.name = '{0}'
        AND a.media_url IS NOT NULL
        AND a.duration {1}= ALL (SELECT 
            a.duration
        FROM
            DbMysql12.Song a,
            DbMysql12.artists b
        WHERE
            a.artist_db_id = b.db_id
                AND b.name = '{0}'
                AND a.media_url IS NOT NULL);""".format(name,op)
    print("query",query)
    con = DBconnection()
    if (con.doSelectQuery(query)):
        con.close()
        return con._columns,con._results
    return None,None

#########ALBUMS OF GENRE ###############################
def albumsOfGenreWithSalesDB(numOfSales,genre):
    query = """SELECT 
    c.name AS Artist_Name,
    a.genre AS Genre,
    COUNT(b.id) AS Num_Of_Albums
FROM
    DbMysql12.Song a,
    DbMysql12.Album b,
    DbMysql12.artists c
WHERE
    b.id = a.album_id AND a.album_id = c.id
        AND b.sales > {0}
        AND a.genre = '{1}'
GROUP BY (b.id)
ORDER BY Num_Of_Albums""".format(numOfSales,genre)
    print("query",query)
    con = DBconnection()
    if (con.doSelectQuery(query)):
        con.close()
        return con._columns,con._results
    return None,None


def mostViewedArtistDB(location,genre):
    query = """
    select * from
(
SELECT artists.name,artists.location, artists.genre,sum(album_views) as artist_views
FROM artists, Album JOIN (SELECT album_id, sum(media_views) as album_views
FROM Song
WHERE media_url is NOT NULL
GROUP BY album_id) as album_by_song
on Album.id = album_by_song.album_id
   WHERE Album.artist_id = artists.id
GROUP BY artists.id, artists.name
ORDER BY artist_views DESC
) t """
    
    if(location != None):
        query += """where t.location like '%"""+location+"""%'"""
        if(genre != None):
            query += """and t.genre like '%"""+genre+"""%'"""
    elif(genre != None):
        query += """where t.genre like '%"""+genre+"""%'"""
  
    con = DBconnection()
    if (con.doSelectQuery(query)):
        con.close()
        return con._columns,con._results
    return None,None    


def addLikedSongDB(song_name,artist_name,user_name):
    query = """
insert into DbMysql12.UserInteraction (user_name,song_id,created_at)
select '"""+user_name+"""' as user_name,s.id as song_id, now()
from DbMysql12.Song s
inner join DbMysql12.artists art
on s.artist_id = art.id
where s.title = '"""+song_name+"""' and art.name = '"""+artist_name+"""'
"""
    
#    f = open('workfile', 'w')
#    f.write(query)
#    f.close()
    con = DBconnection()
    if(con.doQuery(query)):
        print("performed update successfully")
        con.close()
        return True;
    print("error in addLikedSongDB")
    con.close()
    return None;

def personalizationDB(genre,country,longness):
    query = """SELECT 
    a.title AS Song_Name,
    b.name AS Artist_Name,
    a.genre AS Genre,
    a.media_url AS URL
FROM
    DbMysql12.Song a,
    DbMysql12.artists b,
    DbMysql12.CountryArtists c
WHERE
    b.genre = '{0}'
        AND c.name = '{1}'
        AND c.artist_id = b.id
        AND a.artist_id = c.artist_id
        AND a.duration > 240000 * {2}
LIMIT 40;""".format(genre,country,longness)
    print("query",query)
    con = DBconnection()
    if (con.doSelectQuery(query)):
        con.close()
        return con._columns,con._results
    return None,None

def updateYoutubeLinkDB(link,song_name,song_artist):
    query = """
    UPDATE  Song 
SET     media_url = '"""+link+"""'
where title = '""" + song_name+"""' and artist_id = 
(
select id from artists
where name = '"""+song_artist+"""'
)"""
   
    con = DBconnection()
    if(con.doQuery(query)):
        print("performed update successfully")
        con.close()
        return "True";
    print("error in updateYoutubeLinkDB")
    con.close()
    return None;



def getAllSongsDB(user_name):
	pass