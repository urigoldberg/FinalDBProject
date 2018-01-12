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

    
    def connect(self):
        if not (self._open):
            self._db = MySQLdb.connect(user=self._user, db=self._db,  passwd=self._passwd, host=self._host, port = self._port)
            self.cursor = self._db.cursor()
            self._open = True
            
    def selectQuery(self, query):
        
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
        
    def getJsonColumns(self): 
#        num_fields = len(self.cursor.description)
        return [i[0] for i in self.cursor.description]
    
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
    if (con.selectQuery(query) and con._rowsReturned == 1):
        con.close()
        return con._results[0][0]
    return None
 

    

###########GOOGLE API####################
def googleApiSearchSongsByKeyWord(keywords):
    #this is the real query we should be using once we change Lyrics.seed_id to Lyrics.song_id
    #query = 'select s.song_name, s.artist_name, lyr.num_occurrences from (SELECT song_id,((LENGTH(lyrics) - LENGTH(REPLACE(lyrics,'+keyword+', ''))) / LENGTH(' + keyword + ') ) as num_occurrences FROM Lyrics) lyr inner join Songs s on lyr.song_id = s.song_id order by num_occurrences desc limit 3'
    res = '{ "Results": [' 
    
    query = "select t.* from ("
    if len(keywords) == 0:
        return None
    
    for index,keyword in enumerate(keywords):
        if not index == 0:
            query += "union all "
        numOfAppear = 5 - index + 1
        # TO DO - DUPLICATED ROWS
        query += """select * from (SELECT 
        se.title, se.artist_name, lyr.num_occurrences, '"""+keyword+"""' as keyword
    FROM
        (SELECT 
            seed_id,
                ((LENGTH(lyrics) - LENGTH(REPLACE(lyrics, '"""+keyword+"""', ''))) / LENGTH('"""+keyword+"""')) AS num_occurrences
        FROM
            DbMysql12.Lyrics) lyr
            INNER JOIN
        DbMysql12.Seed se ON lyr.seed_id = se.id
    ORDER BY num_occurrences DESC
    LIMIT """+str(numOfAppear) +""") as tbl"""+str(index) +""" 
    """
    con = DBconnection()
    query += ") t where t.num_occurrences > 0 order by t.num_occurrences desc;"
    if (con.selectQuery(query) and con._rowsReturned > 0):
        con.close()
        
        
        for row in con._results:
            song_name = str.format('"%s"' % row[0])
            artist_name = str.format('"%s"' % row[1])
            match = str.format('"%s"' % row[3])
            res += '{ "Song Name":' + song_name + ',"Artist":' + artist_name + ',"YouTube Link":' + '"noooo"' + ', "Matching Keyword":'+match+'},'

#        keyword = str.format('"%s"' % str(keywords))
        return res[:len(res)-1] + ']}'
#        return res[:len(res)-1] + '] , "keyword":'+keyword+'}'
    return None

###########Geographical####################
def geographical_filtering(json):
    res = '{ "Results": [' 
    query = """SELECT 
          artist_name as 'Artist Name', terms as 'Genre', latitude as 'Latitude', longitude as 'Longitude'
           ( 3959 * acos( cos( radians("""+json['latitude']+""") ) * cos( radians( Seed.latitude ) ) 
           * cos( radians(Seed.longitude) - radians("""+json['longitude']+""")) + sin(radians("""+json['latitude']+""")) 
           * sin( radians(Seed.latitude)))) AS distance 
        FROM Seed 
        HAVING distance < """+json['radius']+""" 
        ORDER BY distance;"""

    con = DBconnection()
    if (con.selectQuery(query) and con._rowsReturned > 0):
        cols = con.getJsonColumns()
        for row in con._results:
            res += '{'
            for col,val in zip(cols,row):
               res += '"' + col + '":"' + val + '",'
            res = res[:len(res)-1] + '},'
        con.close()
        
        print("res is", res)            
        return res[:len(res)-1] + ']}'
#        return res[:len(res)-1] + '] , "keyword":'+keyword+'}'
    return None
    
    