import urllib
import urllib.error
import urllib.request
from _mysql_exceptions import Error


import MySQLdb
import json
from tqdm import tqdm


def url_for_record(record):
    parsed = [urllib.parse.quote(s) for s in record]
    # url = 'https://private-anon-9816e48b70-lyricsovh.apiary-mock.com/v1/{}/{}'.format(parsed[0], parsed[1])
    url = 'https://api.lyrics.ovh/v1/{}/{}'.format(parsed[0], parsed[1])
    return url

def insert_lyrics(db_conn, lyrics):
    sql = "UPDATE Song set Song.lyrics = %s WHERE Song.id = %s AND Song.lyrics is NULL "
    try:
        cursur = db_conn.cursor()
        number_of_rows = cur.executemany(sql, lyrics)

        if cursur.lastrowid:
            print('last insert id', cursur.lastrowid)
        else:
            print('last insert id not found')

    except Error as error:
        print(error)

    finally:
        cursur.close()
        db_conn.commit()

    return number_of_rows


db = MySQLdb.connect(host="127.0.0.1",  # your host
                     port=3305,
                     user="DbMysql12",       # username
                     password="DbMysql12",
                     db="DbMysql12")   # name of the database

cur = db.cursor()

cur.execute("SELECT artists.name, title, Song.id FROM Song, artists WHERE Song.artist_id = artists.id and Song.lyrics is NULL ORDER BY artists.name ASC ")
lyrics = []
no_lyrics = []
count = 0
for record in tqdm(cur.fetchall(), desc='Song'):
    url = url_for_record(record[:-1])
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            l = json.loads(html)['lyrics']
            lyrics.append((l, str(record[-1])))
    except urllib.error.HTTPError as err:
        if err.code == 404:
            no_lyrics.append(record[-1])
        else:
            print("record: ", record)
            raise err
    if len(lyrics)%10 == 0:
        insert_lyrics(db, lyrics[-10:])

sql = """UPDATE Song
set Song.lyrics = %s
WHERE Song.id = %s AND Song.lyrics is NULL """
idx = len(lyrics)%10
number_of_rows = cur.executemany(sql, lyrics[idx:])
db.commit()

db.close()


