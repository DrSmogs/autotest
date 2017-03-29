#!/usr/bin/env python

from __future__ import print_function
from future import standard_library


standard_library.install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sys
import getpass
import socket

import time

import logging
logging.basicConfig(level=logging.DEBUG)

#xmpp stuff
from sleekxmpp import Iq, ClientXMPP
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin, ET
from sleekxmpp.exceptions import IqError, IqTimeout

import sleekxmpp
import iq3 #custom stanza stuff for iQ3 unit
from iq3_cmd import iq3_cmd #class and functions for sending iQ3 commands and processing responses

from flask import Flask, request, make_response, render_template #API stuff
from flask_httpauth import HTTPBasicAuth #http auth plugin for flask... need a password!

from config import config # config file for app - make sure you rename config-blank.py and fill out values



# little big of stuff to make it work on both python versions
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

# Flask app should start in global layout
app = Flask(__name__)
auth = HTTPBasicAuth()

users = config.apiusers

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None




# setup the xmpp connection for controlling the iQ3
xmpp = iq3_cmd(config.loginjid, config.loginpw)
xmpp.register_plugin('xep_0030') # Service Discovery
xmpp.register_plugin('xep_0004') # Data Forms
xmpp.register_plugin('xep_0060') # PubSub
xmpp.register_plugin('xep_0199') # XMPP Ping
xmpp.register_plugin('iq3', module=iq3) # custom iQ3 stanza plugin



#main API endpoint for google home
@app.route('/api', methods=['POST'])
@auth.login_required
def api():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@auth.error_handler
def auth_error():
    return "&lt;h1&gt;Access Denied Beeyatch! &lt;/h1&gt;"



def processRequest(req):
    data={}
    try:
        command=req.get('command')
        request=req.get('request')
        boxes = req.get('boxes')


        if command is None:
            return "No command"

        if boxes is None:
            return "No Boxes"

        if request is None:
            return "No request type!"
    except:
        return "Error!!! something went wrong with the request"

    else:
        data['command']=command
        data['request']=request
        data['timestamp']= str(int(time.time()))
        data['results']={}
        if request=='get':

            if command in("error_reporting","diagnostic_hdd","diagnostic_tuner","diagnostic_speed_test","system_information","volume",
                "current_viewing","current_programme","stb_model","dvbt_services","planner_management"):
                 # if if is in a list of supported get stanzas

                for box in boxes:

                    data['results'][box] = xmpp.get_cmd(command,box,'iq3')

            elif command in ("remote_booking", "code_download", "remote_control", "reset_pin", "reboot_stb"):
                 # if its a stanza but does not support a get

                data['error'] = "\'" + command + "\' does not support a get function."

            else:
                data['error'] = "Unknown command \'" + command + "\'."


        elif request=='set':

            #stuff for setting
            data['error']= "Have not implemented set yet"
        else:
            data['error']= "Request must either be a set or get!"

        return data
# once xmpp client is connected - send presence and roster as expected
def session_start(e):
    xmpp.get_roster()
    xmpp.send_presence()


xmpp.add_event_handler('session_start', session_start) # xmpp session start handler

if __name__ == '__main__':
    xmpp.connect() # connect to xmpp server
    xmpp.process(block=False) #process xmpp stuff


    print("Starting app on port %d" % config.serverport)
    app.run(host='0.0.0.0',port=config.serverport)
