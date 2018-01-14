import json

import MySQLdb
import urllib.request
from _mysql_exceptions import Error
from tqdm import tqdm

URL = 'http://www.theaudiodb.com/api/v1/json/1/mvid.php?i={}'

db = MySQLdb.connect(host="127.0.0.1",  # your host
                     port=3305,
                     user="DbMysql12",  # username
                     password="DbMysql12",
                     db="DbMysql12")  # name of the database

cur = db.cursor()

cur.execute("SELECT DISTINCT id, db_id  FROM artists")


def get_mvids_for_artist(artist_id, artist_api_id):
    url = URL.format(artist_api_id)
    mvids = []
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            artist_media = json.loads(html)["mvids"]
            artist_media = artist_media if artist_media is not None else []
            for media in artist_media:
                if "idAlbum" in media:
                    media["artist_id"] = str(artist_id)
                    mvids.append(media)

    except urllib.error.HTTPError as err:
        print("record: ", artist)
        raise err
    return mvids


def sanitize(album_json):
    columns = ('idArtist', 'idAlbum', 'idTrack', 'strMusicVid', 'artist_id', 'idAlbum')

    res = []
    for col in columns:
        col = album_json.get(col)
        if album_json.get(col) is not None:
            res.append(col.lower())
        else:
            res.append(col)
    return tuple(res)


def insert_media_per_artist(db_connection, albums):
    count = 0
    sql = (
        "INSERT INTO Media(artist_db_id, album_db_id, song_db_id, media_url, artist_id, album_id) \n"
        "    VALUES (%s, %s, %s, %s, %s, "
        "(SELECT id from Album where db_id = %s))")
        # (artist_db_id, album_db_id, song_db_id, media_url, artist_id, album_db_id)

    for album in albums:
        try:
            cursur = db_connection.cursor()
            cursur.execute(sql, sanitize(album))

            if cursur.lastrowid:
                count += 1
                print('last insert id', cursur.lastrowid)
            else:
                print('last insert id not found')

        except Error as error:
            print(error)

        finally:
            cursur.close()
            db_connection.commit()
    return count



# artists = [(1, "111822"), (2, "1234534355")]
media = []

for artist in tqdm(cur.fetchall()[-10:], desc="artist"):
    artist_albums = get_mvids_for_artist(*artist)
    media.extend(artist_albums)
    cnt = insert_media_per_artist(db, artist_albums)
    print('inserted: ', cnt)
