#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssl
import sys
import logging
import getpass
import socket
from sleekxmpp import Iq, ClientXMPP
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin, ET
from sleekxmpp.exceptions import IqError, IqTimeout

import sleekxmpp

import iq3 #custom stnza stuff for iQ3 unit

#This contains the iq3 xmpp class as well as the functions you can call. functions will return a dictionary of values



class iq3_cmd(sleekxmpp.ClientXMPP):

    """
    Class for setting up the scorpio login and shit
    this then defines all the functions which go to get spaWned for the mother fucking API
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid



    # return info about current viewing
    def get_current(self, to, resource):

        self.to = to
        self.Resource = resource


        resp= {}
        resp['cmd']='get_current_programme'
        try:
            out = self['iq3'].get_current_programme(self.jid, self.to, self.Resource)

            resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
            resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
            resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
            resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
            resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
            resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

        except IqError as e:

            resp['error_condition'] =str(e.condition)
            resp['error_text'] = str(e.text)
        except IqTimeout:
            resp['error_condition'] = "Box Timeout"


        return resp

    def set_chan(self,channel):
        resp= {}
        resp['cmd']='set_channel'
        resp['error']= None
        resp['channel']=channel
        try:
            out = self['iq3'].set_viewing(self.jid, self.to, self.Resource, channel)
            try:
                resp['error'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}error').text
            except:
                resp['error'] = None

            try:
                resp['response'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}response').text
            except:
                resp['error'] = 'Unknown error'

        except IqError as e:
            resp['error'] = "iq error " + str(e)
        except IqTimeout:
            resp['error'] = "Timeout "

        return resp
