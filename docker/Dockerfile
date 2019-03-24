FROM debian:stretch-slim
MAINTAINER Josu Ruiz <josu@ontro.co.uk>

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip 

WORKDIR /var/www/html/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN export PATH=${PATH}:/usr/lib/python3/dist-packages

ENV SERVER_ENV=Production
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD gunicorn -w 4 -b 0.0.0.0:5001 --access-logfile /var/log/web_restaurant.log restaurant.wsgi
