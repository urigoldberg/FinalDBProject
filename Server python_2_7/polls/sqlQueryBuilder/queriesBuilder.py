import json
import MySQLdb
def get_songs_related_to_keywords(jsons):
    try:
        
        decoded = json.loads(jsons)
        print("here")
        
#        #get all keywords
#        cnt = 0
#        for x in decoded['labelAnnotations']:
##            print (x['description'])
#            cnt += 1
#            if (cnt == 5): 
#                break
        
        keyword = decoded['labelAnnotations'][0]['description']
        print(keyword)
        #this is the real query we should be using once we change Lyrics.seed_id to Lyrics.song_id
#        def_query = 'select s.song_name, s.artist_name, lyr.num_occurrences from (SELECT song_id,((LENGTH(lyrics) - LENGTH(REPLACE(lyrics,'+keyword+', ''))) / LENGTH(' + keyword + ') ) as num_occurrences FROM Lyrics) lyr inner join Songs s on lyr.song_id = s.song_id order by num_occurrences desc limit 3'
        
        #this is a query for making sure it works
        def_query = "select se.title, se.artist_name, lyr.num_occurrences from (SELECT seed_id,((LENGTH(lyrics) - LENGTH(REPLACE(lyrics, 'West', ''))) / LENGTH('West') ) as num_occurrences FROM Lyrics ) lyr inner join Seed se on lyr.seed_id = se.id order by num_occurrences desc limit 3;"
        db = MySQLdb.connect(user='DbMysql12', db='DbMysql12',  passwd='DbMysql12', host='localhost', port = 3305)
        cursor = db.cursor()
        cursor.execute(def_query)
        names = cursor.fetchall()
        print(names)
#        a = cursor.description
        db.close()
    except (ValueError, KeyError, TypeError):
        print ("JSON format error")
        return
    
    
    

string = '{ "labelAnnotations": [{"mid": "/m/015p6","description": "bird","score": 0.9765788,"topicality": 0.9765788},{"mid": "/m/01c4rd","description": "beak","score": 0.953986,"topicality": 0.953986},{"mid": "/m/0gv1x","description": "parrot","score": 0.93232477,"topicality": 0.93232477}]}' 
get_songs_related_to_keywords(string)


#old query
#select se.title, se.artist_name, lyr.num_occurrences
#from (
#	SELECT seed_id,((LENGTH(lyrics) - LENGTH(REPLACE(lyrics, 'West', ''))) / LENGTH('West') ) as num_occurrences
#	  FROM Lyrics
#) lyr
#inner join Seed se
#on lyr.seed_id = se.id
#order by num_occurrences desc
#limit 3