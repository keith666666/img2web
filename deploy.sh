#!/bin/bash

# Define variables
VENV_DIR=".venv"

# reset the git repo to the latest commit
git fetch
git reset --hard origin/main

# Activate the virtual environment
source $VENV_DIR/bin/activate

# install dependencies
pip install -r requirements.txt

# start
gunicorn -c gunicorn_config.py run:app &
