from pymongo import MongoClient
client = MongoClient("mongodb+srv://maxomdal:Cloud2006@cluster0-oyzhb.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

# Get Posts from database by location
def getPosts(longitude, latitude):
    posts = db.inventory.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type":"Point",
                    "coordinates":[longitude,latitude]
                },
                "$maxDistance": 50000
            }
        }
    }).limit(50)
    return list(posts)

# Add new post to database with data being our dictionary representing the post data
def addPost(data, latitude, longitude):
    data["location"] = {"type": "Point", "coordinates":[longitude, latitude]}
    success = db.inventory.insert_one(data)
    if success:
        return True
    else:
        return False