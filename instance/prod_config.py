import os
from datetime import datetime
from dotenv import load_dotenv

INIT_DATA_FILE = 'instance/config/init_data_prod.json'
APP_NAME = 'abagdemo-hs'
now = datetime.now()
DATA_BUCKET_NAME = APP_NAME + '-' + now.strftime('%Y%m%d')
DATA_FILE_NAME = APP_NAME + '.json'
# Load sensitive vars for local development
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)