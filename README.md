This is an archival repo and is not maintained any longer.

py -3 -m venv virtual  # windows

python3 venv virtual # unix

virtual\Scripts\activate

# Run the flask session WINDOWS
virtual\Scripts\activate

set FLASK_APP=employee_directory.py

set FLASK_DEBUG=1

py -3 -m flask run

# Run flask session LINUX
source virtual/bin/activate

export FLASK_APP=employee_directory.py

export FLASK_DEBUG=0

python3 -m flask run

# Initialize the data repository
py -3 -m flask db init

# The First Database Migration
py -3 -m flask db migrate -m "users table"

# Upgrade Database
py -3 -m flask db upgrade

# Flask shell CMD
py -3 -m flask shell



