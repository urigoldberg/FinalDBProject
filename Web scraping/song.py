import json

import MySQLdb
import urllib.request
from _mysql_exceptions import Error
from tqdm import tqdm

URL = 'http://www.theaudiodb.com/api/v1/json/1/track.php?m={}'

db = MySQLdb.connect(host="127.0.0.1",  # your host
                     port=3305,
                     user="DbMysql12",  # username
                     password="DbMysql12",
                     db="DbMysql12")  # name of the database

cur = db.cursor()

cur.execute("SELECT DISTINCT id, db_id  FROM Album where Album.db_id not in (SELECT DISTINCT album_db_id FROM Song)")


def get_songs_for_album(album_id, album_api_id):
    url = URL.format(album_api_id)
    songs = []
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            artist_media = json.loads(html)["track"]
            artist_media = artist_media if artist_media is not None else []
            for media in artist_media:
                if "idAlbum" in media:
                    media["album_id"] = str(album_id)
                    songs.append(media)

    except urllib.error.HTTPError as err:
        print("record: ", album_id)
        raise err
    return songs


def sanitize(album_json):
    columns = ('idTrack', 'idArtist', 'idAlbum', 'lyrics', 'strTrack', 'intDuration', 'strGenre', 'strMusicVid', 'intMusicVidViews', 'intMusicVidLikes', 'intTrackNumber', 'intScore', 'intScoreVotes', 'album_id', 'idArtist')
    # "insert into Song(db_id, artist_db_id, album_db_id, lyrics_id, title, duration, genre, media_id, media_url, media_views, media_likes, order_in_album, score, score_votes, artist_id, album_id) "
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
        "INSERT INTO Song(db_id, artist_db_id, album_db_id, lyrics, title, duration, genre, media_url, media_views, media_likes, order_in_album, score, score_votes, album_id, artist_id) \n"
        "    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
        "(SELECT id from artists where db_id = %s))")

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

for album in tqdm(cur.fetchall(), desc="album"):
    artist_albums = get_songs_for_album(*album)
    media.extend(artist_albums)
    cnt = insert_media_per_artist(db, artist_albums)
    print('inserted: ', cnt)
