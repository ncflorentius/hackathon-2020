import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId
client = MongoClient("mongodb+srv://maxomdal:Cloud2006@cluster0-oyzhb.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Get Posts from database by location
def getPosts(longitude, latitude):
    posts = db.inventory.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type":"Point",
                    "coordinates":[longitude,latitude]
                },
                "$maxDistance": 10000
            }
        }
    }).limit(50).sort([("FavoritesCount", pymongo.DESCENDING)])
    return JSONEncoder().encode({"posts": list(posts)})

# Add new post to database with data being our dictionary representing the post data
def addPost(data, latitude, longitude):
    data["location"] = {"type": "Point", "coordinates":[longitude, latitude]}
    success = db.inventory.insert_one(data)
    if success:
        return True
    else:
        return False


def incrementFavorites(postID):
    result = db.inventory.update({"_id": ObjectId(postID)}, {
        "$inc": {"FavoritesCount": 1}
    })
    print(result)