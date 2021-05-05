import random
import time
from flask import Flask


app = Flask(__name__)


@app.route('/')
def main():
    return "Hello World from Main"

@app.route('/wait')
def wait_endpoint():
    t = round(random.random(), 2)
    time.sleep(t)
    return f"Took {t}s in respond"