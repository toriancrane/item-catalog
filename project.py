from flask import(
    session as login_session,
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template,
    make_response)
from functools import wraps
import random, string
import requests
import jinja2
import httplib2
# import db_methods
import time
import os
import json

#Additional imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Restaurant Menu Application"

#####   User Login Decorator    #####
def login_required(func):
    """
    A decorator to confirm a user is logged in or redirect as needed.
    """
    @wraps(func)
    def check_login(*args, **kwargs):
        # Redirect to login if user not logged in, else execute func.
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return check_login


@app.route('/')
def frontPage():
    return render_template('front.html')





if __name__ == '__main__':
    app.secret_key = 'gDI1tL5OC54UiTF3g18a-bWg'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    #Change this back to be pushed to heroku