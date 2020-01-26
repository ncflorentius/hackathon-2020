from flask import Flask, render_template
import database
app = Flask(__name__)

@app.route('/')
def show_map():
    return render_template('index.html')

@app.route('/<latitude>/<longitude>')
def get_posts_near_loc(latitude, longitude):
    return database.getPosts(float(longitude), float(latitude))