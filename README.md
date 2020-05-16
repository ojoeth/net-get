# Net_get, a minimal flask frontend to youtube-dl
## Dependencies
### System dependencies
* ffmpeg (must be system-wide installation)

### Pip dependencies
* python3
* gunicorn
* flask
* youtube-dl 

All pip dependencies can be installed using:

```
python3 -m pip install -r requirements.txt
```

## Running the server
### With Docker (recommended)
* Git clone this repository
* cd into this repository
* Make sure Docker is installed, and run:

```
docker build -t net_get .
docker run -d --name net_get -p 80:80 net_get:latest
```

### Without Docker
* git clone this repository
* cd into this repository
* install dependencies listed above
* run `gunicorn -b :80 wsgi:app`