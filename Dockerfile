FROM python:3.8.2-alpine3.11
EXPOSE 80
RUN apk update && apk add ffmpeg
ADD . /srv/net-get
WORKDIR /srv/net-get
RUN pip install -r requirements.txt
CMD gunicorn -b :80 wsgi:webapp