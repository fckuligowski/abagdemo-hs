# Use this script to run the app as a developer from the command line
export GOOGLE_APPLICATION_CREDENTIALS=instance/creds/hazel-math-279814.json
#export FLASK_RUN_PORT=30080 # for Linux Academy servers
export FLASK_APP=main.py
source venv/bin/activate
flask run --host=0.0.0.0