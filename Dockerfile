FROM python:3.8.2-alpine3.11
EXPOSE 80
RUN apk update && apk add ffmpeg && apk add redis
ADD . /srv/net-get
WORKDIR /srv/net-get
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/srv/net-get/entrypoint.sh"]
#CMD ["gunicorn", "-b", ":80", "wsgi:webapp"]