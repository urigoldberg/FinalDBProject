import json
import MySQLdb
from collections import OrderedDict
from ..DAL.mainDAL import *

    
def get_songs_related_to_keywords(jsons):

       
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
        #keyword = str(decoded['responses'][0]['labelAnnotations'][0]['description'])
        array = [str(word['description']) for word in decoded['responses'][0]['labelAnnotations']]
        keywords = list(OrderedDict.fromkeys(array))[:5]
        rows = googleApiSearchSongsByKeyWord(keywords)
        
        
    except (ValueError, KeyError, TypeError):
        print ("JSON format error")
    
    return rows

    
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