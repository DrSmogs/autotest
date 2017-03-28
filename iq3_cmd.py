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

    def get_cmd(self, cmd, to, resource):
        self.to = to
        self.Resource = resource
        resp= {}
        resp['command']=cmd

        try:
            out = self['iq3'].get_cmd(cmd, self.jid, self.to, self.Resource)

        except IqError as e:

            resp['error_condition'] =str(e.condition)
            resp['error_text'] = str(e.text)
        except IqTimeout:
            resp['error_condition'] = "Box Timeout"

        else:


        # register_stanza_plugin(Iq, error_reporting)
        # register_stanza_plugin(Iq, diagnostic_hdd)
        # register_stanza_plugin(Iq, diagnostic_tuner)
        # register_stanza_plugin(Iq, diagnostic_speed_test)
        # register_stanza_plugin(Iq, system_information)
        # register_stanza_plugin(Iq, volume)
        # register_stanza_plugin(Iq, current_viewing)
        # register_stanza_plugin(Iq, current_programme)
        # register_stanza_plugin(Iq, remote_control)
        # register_stanza_plugin(Iq, reset_pin)
        # register_stanza_plugin(Iq, reboot_stb)
        # register_stanza_plugin(Iq, code_download)
        # register_stanza_plugin(Iq, stb_model)
        # register_stanza_plugin(Iq, dvbt_services)
        # register_stanza_plugin(Iq, remote_booking)
        # register_stanza_plugin(Iq, epg_managment)
            try: #try and extract the useful info
                if cmd=='error_reporting':

                    resp['error'] = "Not yet implemented" #not yet implemented - need a way to cycle through items

                elif cmd=='diagnostic_hdd':

                    resp['temperature'] = out.xml.find('{foxtel:iq}diagnostic_hdd{foxtel:iq}hdd/{foxtel:iq}temperature').text


                elif cmd=='diagnostic_tuner':

                    resp['error'] = "Not yet implemented" #not yet implemented - need a way to cycle through items

                elif cmd=='diagnostic_speed_test':

                    resp['received'] = out.xml.find('{foxtel:iq}diagnostic_speed_test/{foxtel:iq}speed_test/{foxtel:iq}received').text
                    resp['time'] = out.xml.find('{foxtel:iq}diagnostic_speed_test/{foxtel:iq}Speed_test/{foxtel:iq}time').text

                elif cmd=='system_information':

                    resp['manufacturer'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}manufacturer').text
                    resp['hardware_version'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}hardware_version').text
                    resp['software_version'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}software_version').text
                    resp['serial_number'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}serial_number').text
                    resp['smartcard_number'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}smartcard_number').text
                    resp['fpn_firmware_version'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}fpn_firmware_version').text
                    resp['epg_version'] = out.xml.find('{foxtel:iq}system_information/{foxtel:iq}epg_version').text

                elif cmd=='volume':

                    resp['current_volume'] = out.xml.find('{foxtel:iq}volume/{foxtel:iq}current_volume').text
                    resp['mute'] = out.xml.find('{foxtel:iq}volume/{foxtel:iq}mute').text


                elif cmd=='current_viewing': #need to add in variants for recording and ip.. only braodcast below

                    resp['type'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}type').text
                    resp['lcn'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}lcn').text
                    resp['onid'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}onid').text
                    resp['tsid'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}tsid').text
                    resp['svcid'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}svcid').text
                    resp['servicekey'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}servicekey').text
                    resp['name'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}name').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                elif cmd=='current_programme':

                    resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
                    resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
                    resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
                    resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
                    resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
                    resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

                else:
                    resp['error'] = "Unknown command"


            except:
                resp['error'] = "Stnza reply was different to what was expected"

        return resp









##### old stuff below here ######



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
