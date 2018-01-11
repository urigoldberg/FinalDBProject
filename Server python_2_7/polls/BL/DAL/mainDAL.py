import MySQLdb
import os

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
        
        
        
        
    
    def close(self):
        if (self._open):
            self._db.close()
            self._open = False
        
    
    
    
    