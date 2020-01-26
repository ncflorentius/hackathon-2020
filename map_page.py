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

@app.route('/submit', methods=['POST'])
def publish_post():
    if request.method == 'POST':
        '''create new post'''
        data = request.form # a multidict containing POST data
        database.addPost(data)
    return redirect('/')