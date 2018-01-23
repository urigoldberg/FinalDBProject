# -*- coding: utf-8 -*-
import iso3166
import urllib
import urllib.error
import urllib.request
from _mysql_exceptions import Error
import json
from db import DBconnection

convertions = {
    'RUSSIA': 'RUSSIA',
    'viet nam': 'VIETNAM',
    'IRAN': 'IRAN',
    'VIRGIN ISLANDS, BRITISH': 'BRITISH VIRGIN ISLANDS',
    'VIRGIN ISLANDS, U.S.': 'BRITISH VIRGIN ISLANDS',
    'BRUNEI DARUSSALAM': 'BRUNEI',
    'KOREA, REPUBLIC OF': 'SOUTH KOREA',
    'MACAO': 'MACAU',
    'LAO PEOPLE': 'LAOS',
    'MICRONESIA, FEDERATED STATES OF': 'MICRONESIA',
    'SAINT MARTIN': 'SAINT MARTIN',
    'SYRIA': 'SYRIA',
    'TANZANIA': 'TANZANIA'
}


def insert_row(args):
    query = "INSERT INTO Artist(db_id,name,label,formed_year,year_of_birth,year_of_death,disbanded," \
            "mood,style,genre,website,facebook,twitter,biography,gender,members,location,image,logo)" \
            " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    row_id = 0
    try:
        conn = db
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        row_id = cursor.lastrowid
    except Error as error:
        print(error)

    finally:
        cursor.close()
        return row_id


def get_json_for_artist(artist_name):
    url = "http://www.theaudiodb.com/api/v1/json/1/search.php?s={}".format(urllib.parse.quote(artist_name))
    try:
        with urllib.request.urlopen(url) as response:
            artist_data = response.read()
        res = json.loads(artist_data)['artists']
        if res is not None:
            return json.loads(artist_data)['artists'][0]
        else:
            return None
    except urllib.error.HTTPError as err:
        print(err)
    except RuntimeError as err:
        print(err)

def convert_json_to_tuple_args(artist_json):
    columns = [artist_json['idArtist'],artist_json['strArtist'], \
               artist_json['strLabel'],artist_json['intFormedYear'], \
               artist_json['intBornYear'],artist_json['intDiedYear'],artist_json['strDisbanded'], \
               artist_json['strMood'],artist_json['strStyle'],artist_json['strGenre'], \
               artist_json['strWebsite'],artist_json['strFacebook'],artist_json['strTwitter'], \
               artist_json['strBiographyEN'],artist_json['strGender'],artist_json['intMembers'], \
               artist_json['strCountry'],artist_json['strArtistThumb'],artist_json['strArtistLogo'] \
               ]
    res = []
    for col in columns:
        if col is not None:
            res.append(col.lower())
        else:
            res.append(col)
    return tuple(res)


def get_artists_by_country(country, url):
    url = url.format(urllib.parse.quote(country))
    artists = []
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            response = json.loads(html).get('topartists')
            if response is not None:
                response = response.get('artist')
                artists = [artist.get('name') for artist in response]
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print('bat country name')
        raise err
    return artists


def get_missing_artist_from_audb(artist):
    row_id = -1
    artist_json = get_json_for_artist(artist)
    if artist_json is not None:
        row_data_tuple = convert_json_to_tuple_args(artist_json)
        row_id = insert_row(row_data_tuple)
    return row_id


def search_for_artists(db_conn, artists):
    q = "select name from Artist WHERE LOWER(name) = LOWER(%s)"
    existing_artists = set()
    for artist in artists:
        try:
            cursor = db_conn.cursor()
            cursor.execute(q, (artist,))
            record = cursor.fetchone()
            record = record[0] if record is not None else ''
            existing_artists.add(record)
            cursor.close()
        except Error as error:
            print(error)
            cursor.close()

    non_existing_artists = set([artist.lower() for artist in artists]) - set(existing_artists)
    for artist in non_existing_artists:
        get_missing_artist_from_audb(artist)

def insert_country_artist(conn, country, artists):
    q =  ("INSERT INTO CountryArtists(name, artist_id) \n"
          "VALUES (%s, (SELECT  id from Artist where LOWER(Artist.name) = LOWER(%s) limit 1))")
    for artist in artists:
        try:
            cursor = conn.cursor()
            cursor.execute(q, (country, artist))
            conn.commit()
            row_id = cursor.lastrowid
            print("inserted: ", row_id)
            cursor.close()
        except Error as error:
            print(error)
            print('error in country: %s, artist: %s' % (country, artist))


def get_existing_countries(db):
    q = "select DISTINCT name from CountryArtists"
    try:
        cursor = db.cursor()
        cursor.execute(q)
        records = cursor.fetchall()
        cursor.close()
    except Error as error:
        print(error)

    return list(records)

def rename_country(country):
    best_name = country
    for x in convertions.keys():
        if x in country:
            best_name = convertions[x]
    return best_name


db = DBconnection().connect()
cur = db.cursor()
URL = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={}&api_key=c8c6ea9f0b8ccb1a4cbf60296706e87e&format=json'
visited_countries = get_existing_countries(db)

for country in list(iso3166.countries_by_name.keys()):
    if (country,) in visited_countries:
        continue
    country = rename_country(country)
    artists = get_artists_by_country(country, URL)
    search_for_artists(db, artists)
    insert_country_artist(db, country, artists)

