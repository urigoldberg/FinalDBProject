import urllib
import urllib.error
import urllib.request

import MySQLdb
import json
import csv
from tqdm import tqdm


def url_for_record(record):
    parsed = [urllib.parse.quote(s) for s in record]
    # url = 'https://private-anon-9816e48b70-lyricsovh.apiary-mock.com/v1/{}/{}'.format(parsed[0], parsed[1])
    url = 'https://api.lyrics.ovh/v1/{}/{}'.format(parsed[0], parsed[1])
    return url

def flush_to_csv(file, lyrics):
    with open(file, 'a') as csvfile:
        writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in lyrics:
            writer.writerow(line[:-1])


db = MySQLdb.connect(host="127.0.0.1",  # your host
                     port=3305,
                     user="DbMysql12",       # username
                     password="DbMysql12",
                     db="DbMysql12")   # name of the database
# db = MySQLdb.connect(host="localhost",  # your host
#                      user="root",       # username
#                      db="uni")   # name of the database

# Create a Cursor object to execute queries.
cur = db.cursor()

cur.execute("SELECT DISTINCT artist_name, title, id  FROM Seed")
lyrics = []
no_lyrics = []
file = '/Users/orrbarkat/repos/sql_project/Web scraping/lyrics.csv'
for record in tqdm(cur.fetchall()[611+3060+220:], desc='Song'):
    url = url_for_record(record[:-1])
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            l = json.loads(html)['lyrics']
            lyrics.append([l, record[-1], record[-1]])
    except urllib.error.HTTPError as err:
        if err.code == 404:
            no_lyrics.append(record[-1])
        else:
            print("record: ", record)
            raise err
    if len(lyrics) % 20 == 0:
        flush_to_csv(file, lyrics[-20:])
idx = len(lyrics)%20
flush_to_csv(file, lyrics[idx:])


#
# sql = """INSERT INTO Lyrics(lyrics, seed_id)
# SELECT * FROM (SELECT %s, %s) AS tmp
# WHERE NOT EXISTS (
#     SELECT seed_id FROM Lyrics WHERE seed_id = %s
# ) LIMIT 1;"""
#
# number_of_rows = cur.executemany(sql, lyrics)
# db.commit()
#
# db.close()


