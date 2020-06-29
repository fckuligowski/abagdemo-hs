from . import bags_blueprint
from flask import current_app, request
import flask
import json
from google.cloud import storage
from google.cloud.storage import Blob

@bags_blueprint.route('/')
@bags_blueprint.route('/index')
def index():
    return 'Welcome to the %s application. Version=%s\n' % (
        current_app.config.get('APP_NAME'), get_version())

def get_version():
    """
        Read the version number from the version.txt file, which the
        code pipeline has placed in the cwd. Or show 'unknown' if
        we can't find the file.
    """
    rtn = 'unknown'
    try:
        with open('version.txt', 'r') as file:
            instr = file.read().replace('\n', '')
            instrs = instr.split(':')
            rtn = instrs[-1]
    except Exception as e:
        pass
    return rtn

@bags_blueprint.route('/scan', methods=['POST'])
def scan():
    rtn = {
        'scan': ''
    }
    if request.method == 'POST':
        scan = request.get_json()
        rtn['scan'] = save_bag_scan(scan)
    return rtn

@bags_blueprint.route('/status')
@bags_blueprint.route('/status/<bag_id>')
def status(bag_id=None):
    """
        Return the last element for the specified bag.
    """
    data_dict = get_bag_data(bag_id)
    rtn = ''
    if len(data_dict):
        rtn = json.dumps(data_dict[-1], indent=4)
    elif bag_id is not None:
        flask.abort(404)
    return rtn

@bags_blueprint.route('/history')
@bags_blueprint.route('/history/<bag_id>')
def history(bag_id=None):
    """
        Return all the elements for the specified bag
    """
    data_dict = get_bag_data(bag_id)
    rtn = ''
    if len(data_dict):
        rtn = json.dumps(data_dict, indent=4)
    elif bag_id is not None:
        flask.abort(404)
    return rtn

def get_bag_data(bag_id):
    """
        Retrieve the data from the storage bucket
        and then filter by the specified bag_id
    """
    data_dict, _ = get_data()
    if bag_id is None:
        bag_id = '000'
    rtn = []
    for data_item in data_dict:
        if data_item['bag'] == bag_id:
            rtn.append(data_item)
    return rtn

def save_bag_scan(scan):
    """
        Add the supplied scan to the end of the data file.
        Returns back an integer with the number scan that this
        supplied scan is in the file (array index).
    """
    data_dict, blob = get_data()
    # Add record to end of data
    data_dict.append(scan)
    print(json.dumps(data_dict, indent=4))
    # Save the data back to GCP storage
    blob.upload_from_string(json.dumps(data_dict, indent=4))
    return len(data_dict)

def get_data():
    """
       Retrieve the data file from GCP Storage, and return
       the file as a dictionary.
       Create the file, with dummy data, if it don't exist.
    """
    rtn = None
    storage_client = storage.Client()
    bucket_name = current_app.config.get('DATA_BUCKET_NAME')
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except Exception as e:
        bucket = storage_client.create_bucket(bucket_name)
    # Test if the data file is found in the bucket, and
    # create it if it doesn't exist.
    blob = Blob(current_app.config.get('DATA_FILE_NAME'), bucket)
    if not blob.exists():
        # Open the initial data file
        init_fname = current_app.config.get('INIT_DATA_FILE')
        with open(init_fname) as infile:
            init_data = json.load(infile)
        # Copy it to the storage bucket
        blob.upload_from_string(json.dumps(init_data, indent=4))
    data_str = blob.download_as_string()
    rtn = json.loads(data_str)
    return rtn, blob
