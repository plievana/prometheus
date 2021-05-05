import random
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from prometheus_client import make_wsgi_app, Counter, Histogram


app = Flask(__name__)


c = Counter("flask_app_sample_metric", "Sample metric for prometheus tutorial")
h = Histogram("flask_app_sample_histogram", "Sample histogram for prometheus tutorial")
d = Counter("flask_app_sample_devices", "Sample counter opts devices for prometheus tutorial", ["device"])


@app.route('/')
def main():
    c.inc()
    h.observe(random.random())
    d.labels(device='/dev/sda').inc()
    return "Hello Worlda"


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
