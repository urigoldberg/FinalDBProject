import MySQLdb
import os

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

    
    def connect(self):
        if not (self._open):
            self._db = MySQLdb.connect(user=self._user, db=self._db,  passwd=self._passwd, host=self._host, port = self._port)
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
            self._succ = True
            self._results = self.cursor.fetchall()
            self._columns = [i[0] for i in self.cursor.description]
            return True
        
        # fail
        except Exception as e:
            self._exception = (e.message)
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
    
def addNewUserDAL(username, password):
    query = """insert into DbMysql12.users_table values ('"""+username+"""','"""+password+"""');"""
    con = DBconnection()
    if (con.insertQuery(query)):
        con.close()
        return True
    
    con.close()
    print(con._exception)
    return False


def getUserPasswordUsernameDAL(username):
    query = "select password from DbMysql12.users_table where user_name = '"+username+"';";
    con = DBconnection()
    if (con.doSelectQuery(query) and con._rowsReturned == 1):
        con.close()
        return con._results[0][0]
    return None
 

    

###########GOOGLE API####################
    
def googleApiSearchSongsByKeyWord(keywords):
    #this is the real query we should be using once we change Lyrics.seed_id to Lyrics.song_id    
    keywords_for_full_text = ""
    for keyword in keywords:
        keywords_for_full_text += ' +'+ keyword
    query = """
    create table DbMysql12.temp_keywords
(
	song_id int,
    lyrics text
);

Insert Into DbMysql12.temp_keywords
SELECT lyr.song_id ,lyr.lyrics FROM DbMysql12.Lyrics lyr
where match(lyr.lyrics) against ('"""+keywords_for_full_text+"""' in boolean mode);
    """
    query += "select t.* from ("
    if len(keywords) == 0:
        return None
    
    for index,keyword in enumerate(keywords):
        if not index == 0:
            query += "union all "
        numOfAppear = 5 - index + 1
        # TO DO - DUPLICATED ROWS
        query += """select * from (SELECT 
    inner_songs.title, art.name, inner_songs.num_occurrences, '"""+keyword+"""' as keyword
FROM
    (SELECT 
        *
    FROM
        (SELECT 
        song_id,
            ((LENGTH(lyrics) - LENGTH(REPLACE(lyrics, '"""+keyword+"""', ''))) / LENGTH('"""+keyword+"""')) AS num_occurrences
    FROM
        DbMysql12.temp_keywords) lyr
    INNER JOIN DbMysql12.Song son ON lyr.song_id = son.id)  inner_songs
        INNER JOIN
    DbMysql12.artists art ON art.db_id = inner_songs.artist_db_id
ORDER BY num_occurrences DESC
LIMIT """+str(numOfAppear) +""") as tbl"""+str(index) +""" 
    """
    con = DBconnection()
    query += """) t where t.num_occurrences > 0 order by t.num_occurrences desc;
    drop table DbMysql12.temp_keywords;"""
    if (con.doSelectQuery(query) and con._rowsReturned > 0):
        con.close()
        return con._results 
    return None

###########Geographical####################
def geographical_filtering(json):

    query = """SELECT 
          artist_name as 'Artist Name', terms as 'Genre', latitude as 'Latitude', longitude as 'Longitude'
           ( 3959 * acos( cos( radians("""+json['latitude']+""") ) * cos( radians( Seed.latitude ) ) 
           * cos( radians(Seed.longitude) - radians("""+json['longitude']+""")) + sin(radians("""+json['latitude']+""")) 
           * sin( radians(Seed.latitude)))) AS distance 
        FROM Seed 
        HAVING distance < """+json['radius']+""" 
        ORDER BY distance;"""

    con = DBconnection()
    if (con.doSelectQuery(query) and con._rowsReturned > 0):
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
    AND t.genre like '{2}'
        AND t.genre IS NOT NULL
        AND t.genre NOT LIKE ''
GROUP BY t.genre
HAVING numOfArts > {1}
ORDER BY numOfArts DESC;""".format(dead,num,genre)
    print("query",query)
    con = DBconnection()
    if (con.doSelectQuery(query) and con._rowsReturned > 0):
        con.close()
        return con._columns,con._results
    return None,None