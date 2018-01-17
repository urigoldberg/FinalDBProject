from ..DAL.mainDAL import geographical_filtering
from ..GenericBL.GenericBL import generateResFromRes

def get_artists_in_requested_radius(json):
    print("in get_artists_in_requested_radius")
    print(json)
    longitude, latitude, radius = str(json["longitude"]),str(json["latitude"]),str(json["radius"])
    cols,result = geographical_filtering(longitude, latitude, radius)
    if(cols == None):
        return '[{"no results were found. you are welcome to mark a new location on the map": ""}]'
    return generateResFromRes(cols,result)