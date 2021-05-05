FROM python:3.7

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

VOLUME /app

WORKDIR /app


EXPOSE 5000

CMD gunicorn --statsd-host=statsd:9125 --statsd-prefix=helloworld --bind=0.0.0.0:5000 main:app
