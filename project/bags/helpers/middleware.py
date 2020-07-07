# These are the main helper functions for Prometheus. I got them from:
# https://rollout.io/blog/monitoring-your-synchronous-python-web-applications-using-prometheus/
# and https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_prometheus
# They provide a Count metric and Histogram metric for the app, which count
# the number of requests for the app, and the duration of the requests.
# These get attached to the Flask application object in bags/__init__.py, and
# from there the metrics are magically provided by prometheus_client.
from flask import current_app, request
from prometheus_client import Counter, Histogram
import time
import sys

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels(current_app.config.get('APP_NAME'), request.path).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels(current_app.config.get('APP_NAME'), request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)