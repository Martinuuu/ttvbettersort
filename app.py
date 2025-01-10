from flask import Flask, redirect, url_for, render_template
import api
    
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/clips/<streamer>")
def showClips(streamer):
    clips = api.getClips(streamer)
    sorted_clips = sorted(clips, key=lambda x: x.unix_created_at, reverse=True)
    return render_template('clips.html.jinja', clips=sorted_clips, streamer=streamer)

@app.route("/data/<streamer>")
def data(streamer):
    clips = api.getClips(streamer, True)
    return clips

@app.route("/id/<name>")
def streamer_id(name):
    return api.getStreamerID(name)

@app.route("/clips/")
def clips_redirect():
    return redirect('/')

