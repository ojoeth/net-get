from flask import Flask, escape, request, render_template, send_from_directory, Response, redirect
from hashlib import sha256
from celery import Celery
from os import path as ospath
import youtube_dl

celery = Celery('net_get', broker='redis://redis:6379/0')
webapp = Flask(__name__)

def make_filename(url, videoformat):
    # Set file name as a sha256 has of the URL
    filename = (sha256(url.encode()).hexdigest() + "." + videoformat)
    fetch_video.delay(url, videoformat, filename)
    return filename

@celery.task
def fetch_video(url, videoformat, filename):
    ydl_opts = {'verbose':True, 'outtmpl': ('content/'+filename), 'prefer_ffmpeg': True, } # Set output template for Youtube-DL
    
    ## Check requested video format and appropriate options
    if videoformat == "mp3":
        ydl_opts.update({'format': 'bestaudio', "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]})
    elif videoformat == "mp4":
        ydl_opts.update({'format':'mp4', 'merge_output_format':'mp4'})
    
    ## Download URL
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@webapp.route('/')
def main_page():
    return render_template('index.html')

@webapp.route('/styles.css')
def serve_styles():
    styles = render_template('styles.css')
    return Response(styles, mimetype='text/css')

@webapp.route('/download', methods=['GET', 'POST'])
def download_video():
    origin = request.headers.get('Origin')

    if request.method == 'POST':
        path = make_filename(request.form.get('url'), request.form.get('videoformat'))
        return render_template('content.html', path=path, origin=origin)
    else:
        return redirect("..", code=302)

@webapp.route('/content/<path:path>')
def serve_content(path):
    if ospath.exists(("content/"+path)):
        return send_from_directory('content', path)
    elif ospath.exists(("content/"+path+".part")):
        return render_template('not_ready.html')
    else:
        return render_template("404.html"), 404
