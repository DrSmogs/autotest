#!/usr/bin/python
# -*- coding: utf-8 -*-

#Config file - saves settings for logging in. This should be part of .gitignore so it's not published
#
class config:

    xmppdomain = 'xmpp.iamshaw.net'
    #xmppdomain = 'xmpp.thomasholtdrive.com'
    loginjid = 'james' #username for the app to log into xmpp server
    loginpw = 'TryAgain10' # pass word for app to logiunn to xmpp server
    reqtimeout = 100
    #loginpw = 'jamesisawesome' # pass word for app to logiunn to xmpp server
    boxloginpart =''
    #boxloginpart ='.iq3.xmpp.thomasholtdrive.com'
    resource = 'iq3' # resource for the iQ3 unit - will alkways be iQ3
    serverport = 5000 #port to run the server on
    apiusers= {
        "cpeadmin": "Foxtel01",
        "James": "isawesome"
    }
