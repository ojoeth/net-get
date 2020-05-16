from flask import Flask, escape, request, render_template, send_from_directory, Response
from hashlib import sha256
import youtube_dl

app = Flask(__name__)

def grab_video(url, videoformat):
    # Set file name as a sha256 has of the URL
    filename = (sha256(url.encode()).hexdigest() + "." + videoformat)

    ydl_opts = {'verbose':True, 'outtmpl': ('content/'+filename), 'prefer_ffmpeg': True, } # Set output template for Youtube-DL
    
    ## Check requested video format and appropriate options
    if videoformat == "mp3":
        ydl_opts.update({'format': 'bestaudio', "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]})
    elif videoformat == "mp4":
        ydl_opts.update({'format':'mp4', 'merge_output_format':'mp4'})
    else:
        return 400, "invalid format!"
    
    ## Download URL
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return filename

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/styles.css')
def serve_styles():
    styles = render_template('styles.css')
    return Response(styles, mimetype='text/css')

@app.route('/download', methods=['GET', 'POST'])
def download_video():
    origin = request.headers.get('Origin')
    path = grab_video(request.form.get('url'), request.form.get('videoformat'))
    return render_template('content.html', path=path, origin=origin)

@app.route('/content/<path:path>')
def serve_content(path):
    return send_from_directory('content', path)
