#!/usr/bin/python
# -*- coding: utf-8 -*-

#Config file - saves settings for logging in. This should be part of .gitignore so it's not published
#
class config:

    xmppdomain = 'xmpp.thomasholtdrive.com'
    loginjid = 'james' #username for the app to log into xmpp server
    loginpw = 'jamesisawesome' # pass word for app to logiunn to xmpp server
    boxloginpart ='.iq3.xmpp.thomasholtdrive.com'
    resource = 'iq3' # resource for the iQ3 unit - will alkways be iQ3
    apiusername = 'cpeadmin' #username to access the api
    apipassword = 'Foxtel01' #password to access the api
    serverport = 5000 #port to run the server on
    apiusers= {
        "cpeadmin": "Foxtel01",
        "James": "isawesome"
    }
    tojid='boxymcboxface@xmpp.iamshaw.net'
