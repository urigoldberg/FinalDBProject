import json
import MySQLdb
from ..DAL.mainDAL import *


def get_songs_related_to_keywords(jsons):

    res = '{ "Results": ['    
    keyword = None
    
    try:
        decoded = json.loads(jsons)
#        #get all keywords
#        cnt = 0
#        for x in decoded['labelAnnotations']:
##            print (x['description'])
#            cnt += 1
#            if (cnt == 5): 
#                break
        keyword = str(decoded['responses'][0]['labelAnnotations'][0]['description'])
        rows = googleApiSearchSongsByKeyWord(keyword)
        
        for row in rows:
            song_name = str.format('"%s"' % row[0])
            artist_name = str.format('"%s"' % row[1])
            res += '{ "song_name":' + song_name + ',"artist_name":' + artist_name + ',"youtube_link":' + '"noooo"' + '},'

        
    except (ValueError, KeyError, TypeError):
        print ("JSON format error")
    keyword = str.format('"%s"' % keyword)
    return res[:len(res)-1] + '] , "keyword":'+keyword+'}'

    
#
#string = '{ "labelAnnotations": [{"mid": "/m/015p6","description": "bird","score": 0.9765788,"topicality": 0.9765788},{"mid": "/m/01c4rd","description": "beak","score": 0.953986,"topicality": 0.953986},{"mid": "/m/0gv1x","description": "parrot","score": 0.93232477,"topicality": 0.93232477}]}' 
#get_songs_related_to_keywords(string)


 
        #this is a query for making sure it works
#        def_query = "select se.title, se.artist_name, lyr.num_occurrences from (SELECT seed_id,((LENGTH(lyrics) - LENGTH(REPLACE(lyrics, 'West', ''))) / LENGTH('West') ) as num_occurrences FROM Lyrics ) lyr inner join Seed se on lyr.seed_id = se.id order by num_occurrences desc limit 3;"

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