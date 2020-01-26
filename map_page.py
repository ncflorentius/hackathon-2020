from flask import Flask, render_template, request, redirect
import database
app = Flask(__name__)

@app.route('/')
def show_map():
    return render_template('index.html')

@app.route('/<latitude>/<longitude>')
def get_posts_near_loc(latitude, longitude):
    return database.getPosts(float(longitude), float(latitude))

@app.route('/create')
def create_post():
    return render_template('addPage.html')

@app.route('/create/submit/', methods=['POST'])
def publish_post():
    if request.method == 'POST':
        '''create new post'''
        data = request.get_json() # a multidict containing POST data
        data["FavoritesCount"] = 0
        lat = data.pop("lat")
        lng = data.pop("lng")
        database.addPost(data, lat, lng)
        print(data)
        print("created new entry in database")
    return redirect('/')