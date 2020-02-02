from flask import Flask, render_template, request, redirect, jsonify
from flask_debug import Debug
import database
import json
application = api = Flask(__name__)

@application.route('/')
def show_map():
    return render_template('index.html')

@application.route('/<latitude>/<longitude>')
def get_posts_near_loc(latitude, longitude):
    return database.getPosts(float(longitude), float(latitude))

@application.route('/create')
def create_post():
    return render_template('addPage.html')

@application.route('/create/submit/', methods=['POST'])
def publish_post():
    if request.method == 'POST':
        '''create new post'''
        data = request.get_json()
        data["FavoritesCount"] = 0
        lat = data.pop("lat")
        lng = data.pop("lng")
        database.addPost(data, lat, lng)
        print("created new entry in database")
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

@application.route('/favorited/<postID>')
def favorite_post(postID):
    if request.method == 'GET':
        '''favorite the post with id'''
        database.incrementFavorites(postID)
    return redirect('/')

@application.route('/feed/<latitude>/<longitude>')
def show_feed(latitude, longitude):
    posts = database.getPosts(float(longitude), float(latitude))
    posts = json.loads(posts)
    for post in posts["posts"]:
        post["location"]["coordinates"][0] = "%.2f" % post["location"]["coordinates"][0]
        post["location"]["coordinates"][1] = "%.2f" % post["location"]["coordinates"][1]
    return render_template('feed.html', posts=posts["posts"])

if __name__ == "__main__":
    application.debug = True
    Debug(application)
    application.run(ssl_context='adhoc')