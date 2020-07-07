#
# This creates the application, and registers
# any Blueprints that it needs.
#
from flask import Flask
from .bags.helpers.middleware import setup_metrics
import json
import sys
from google.cloud import storage
from google.cloud.storage import Blob

# Create any global variables here

def create_app(config_filename=None):
    """
       Create the application and register Blueprints
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    setup_metrics(app)
    return app

def initialize_extensions(app):
    """
       Create the storage bucket and file that we will
       use for our testing data.
    """
    # Test the Google Cloud Storage credentials
    try:
        storage_client = storage.Client()
        for bucket in storage_client.list_buckets(max_results=1):
            tmp = bucket
    except Exception as e:
        msg = "Unable to access Google Storage data due to error: %s." % str(e)
        print(msg)
        sys.exit(1)

def register_blueprints(app):
    from project.bags import bags_blueprint

    app.register_blueprint(bags_blueprint)