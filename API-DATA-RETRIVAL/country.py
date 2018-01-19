from _mysql_exceptions import Error
from db import DBconnection
import json


def filter_json(data):
    cols = ('region', 'subregion', 'capital', 'cca3')
    res = [data.get('name').get('common')]
    res.extend(data.get('latlng'))

    for col in cols:
        if data.get(col) is not None:
            res.append(data.get(col))
        else:
            res.append(col)
    return tuple(res)

def insert_rows(db, args):
    q = 'insert into Country(name, latitude, longitude, region, subregion, capital, cca3) ' \
        'VALUES (upper(%s), %s, %s, %s, %s, %s, %s)'
    try:
        conn = db
        cursor = conn.cursor()
        cursor.executemany(q, args)
        conn.commit()
        row_id = cursor.lastrowid
    except Error as error:
        print(error)
        row_id = -1
    finally:
        cursor.close()
        print(row_id)
        return row_id

with open('countries.json', 'r') as f:
    data = json.load(f)

db = DBconnection().connect()

for country in data[0:1]:
    args = map(filter_json, data)
    insert_rows(db, args)
