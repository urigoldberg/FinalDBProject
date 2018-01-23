import json
import urllib.request
from _mysql_exceptions import Error
from db import DBconnection
from tqdm import tqdm

db = DBconnection().connect()

cur = db.cursor()

cur.execute("SELECT DISTINCT id, db_id  FROM Artist where db_id not in (SELECT DISTINCT artist_db_id FROM Album)")


def get_albums_for_artist(artist_id, artist_api_id):
    url = URL.format(artist_api_id)
    albums = []
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            artist_albums = json.loads(html)["album"]
            artist_albums = artist_albums if artist_albums is not None else []
            for album in artist_albums:
                if "idAlbum" in album:
                    album["artist_id"] = str(artist_id)
                    albums.append(album)

    except urllib.error.HTTPError as err:
        print("record: ", artist)
        raise err
    return albums


def sanitize(album_json):
    columns = ('idAlbum', 'idArtist', \
               'strAlbum', 'intYearReleased', \
               'strStyle', 'strGenre', 'intSales', \
               'strAlbumThumb', 'strAlbumCDart', 'strDescriptionEN', \
               'intScore', 'intScoreVotes', 'artist_id')

    res = []
    for col in columns:
        col = album_json.get(col)
        if album_json.get(col) is not None:
            res.append(col.lower())
        else:
            res.append(col)
    return tuple(res)


def insert_albums_per_artist(db, albums):
    count = 0
    sql = (
        "INSERT INTO Album(db_id, artist_db_id, name, release_year, style, genre, sales, thumb_url, Album_art_url, description, score, votes, artist_id) \n"
        "    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    # "    VALUES ({idAlbum}, {idArtist}, {strAlbum}, {intYearReleased}, {strStyle}, {strGenre}, {intSales}, {strAlbumThumb}, {strAlbumCDart}, {strDescriptionEN}, {intScore}, {intScoreVotes}, {artist_id})")

    for album in albums:
        try:
            cur = db.cursor()
            cur.execute(sql, sanitize(album))

            if cur.lastrowid:
                count += 1
                print('last insert id', cur.lastrowid)
            else:
                print('last insert id not found')

        except Error as error:
            print(error)

        finally:
            cur.close()
            db.commit()
    return count


URL = 'http://www.theaudiodb.com/api/v1/json/1/album.php?i={}'

albums = []
ids = set()

file = '/Users/orrbarkat/repos/sql_project/Web scraping/albums.csv'

for artist in tqdm(cur.fetchall(), desc='Artist'):
    artist_albums = get_albums_for_artist(*artist)
    albums.extend(artist_albums)
    cnt = insert_albums_per_artist(db, artist_albums)
    print('inserted: ', cnt)
