import urllib
import urllib.error
import urllib.request
from _mysql_exceptions import Error
from db import DBconnection
import json
from tqdm import tqdm

def url_for_record(record):
    parsed = [urllib.parse.quote(s) for s in record]
    url = 'https://api.lyrics.ovh/v1/{}/{}'.format(parsed[0], parsed[1])
    return url

def insert_lyrics(db_conn, lyrics):
    sql = "INSERT INTO Lyrics(lyrics, song_id) VALUES (%s, %s)"
    number_of_rows = 0
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


db = DBconnection().connect()

cur = db.cursor()

cur.execute("SELECT artists.name, title, Song.id "
            "FROM Song, artists "
            "WHERE Song.artist_id = artists.id "
            "and Song.id != ALL ("
            "SELECT song_id FROM Lyrics)")
lyrics = []
no_lyrics = []
count = 0
for record in tqdm(cur.fetchall(), desc='Lyrics'):
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
    if len( lyrics ) % 10 == 0:
        insert_lyrics(db, lyrics[-10:])

idx = len( lyrics ) % 10
insert_lyrics(db, lyrics[-idx:])

