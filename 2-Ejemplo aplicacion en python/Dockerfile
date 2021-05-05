FROM python:3.7

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

VOLUME /app

WORKDIR /app


ENV FLASK_APP=/app/main.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD flask run --host=0.0.0.0
