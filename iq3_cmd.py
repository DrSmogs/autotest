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
import config
from config import sleekxmpp

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

    def get_cmd(self, cmd, box, resource):
        self.to = box+config.boxloginpart+'@'+config.xmppdomain
        self.Resource = resource
        resp= {}
        resp['box_id'] = box

        try:
            out = self['iq3'].get_cmd(cmd, self.jid, self.to, self.Resource)

        except IqError as e:

            resp['error'] =str(e.condition)

        except IqTimeout:
            resp['error_condition'] = "Box Timeout"

        else:
            # items not yet implemented
            # error_reporting - not implemented - i dont think this is working on the box?

            # dvbt_services - Not Tested - returning no results from box
            # planner_managment - item cycling needed

            # register_stanza_plugin(Iq, epg_managment)

            try: #run the extract commands - return an error if they don't work

                if cmd=='error_reporting':

                    resp['error_report'] = out.xml.findall('{foxtel:iq}error_reporting/{foxtel:iq}error').text #not implemented??

                elif cmd=='diagnostic_hdd':
                    resp['temperature'] = out.xml.find('{foxtel:iq}diagnostic_hdd/{foxtel:iq}hdd/{foxtel:iq}temperature').text

                elif cmd=='diagnostic_tuner':
                    resp['tuners'] = []
                    tuners=out.xml.findall('{foxtel:iq}diagnostic_tuner/{foxtel:iq}tuner')
                    for tuner in tuners:
                        tunerdict={}
                        tunerdict['tuner_number'] = tuner.find('{foxtel:iq}tuner_number').text
                        tunerdict['frequency'] = tuner.find('{foxtel:iq}frequency').text
                        tunerdict['type'] = tuner.find('{foxtel:iq}type').text
                        tunerdict['locked'] = tuner.find('{foxtel:iq}locked').text
                        try:
                            tunerdict['level_dBm'] = tuner.find('{foxtel:iq}level').text
                            quality = tuner.findall('{foxtel:iq}quality')

                        except:
                            tunerdict['level_dBm'] = 'N/A'
                            tunerdict['quality_snr_db'] = 'N/A'
                            tunerdict['quality_uncorrected_ber'] = 'N/A'

                        else:
                            for qual in quality:

                                if qual.attrib['type']=="signal_to_noise":
                                    tunerdict['quality_snr_db'] = qual.text

                                elif qual.attrib['type']=="uncorrected_BER":
                                    tunerdict['quality_uncorrected_ber'] = qual.text

                                elif qual.attrib['type']=="corrected_BER":
                                    tunerdict['quality_corrected_ber'] = qual.text

                        resp['tuners'].append(tunerdict)

                elif cmd=='diagnostic_speed_test':
                    resp['received'] = out.xml.find('{foxtel:iq}diagnostic_speed_test/{foxtel:iq}speed_test/{foxtel:iq}received').text
                    resp['time'] = out.xml.find('{foxtel:iq}diagnostic_speed_test/{foxtel:iq}speed_test/{foxtel:iq}time').text

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

                elif cmd=='stb_model':
                    resp['model'] = out.xml.find('{foxtel:iq}stb_model/{foxtel:iq}model').text #This works in the API - but not working on the box

                elif cmd=='dvbt_services':
                    resp['services'] = []
                    services=out.xml.findall('{foxtel:iq}dvbt_services/{foxtel:iq}service')
                    for service in services:
                        servicedict={}
                        servicedict['onid'] = service.find('{foxtel:iq}onid').text
                        servicedict['service_key'] = service.find('{foxtel:iq}service_key').text
                        servicedict['svc_name'] = service.find('{foxtel:iq}svc_name').text
                        servicedict['svcid'] = service.find('{foxtel:iq}svcid').text
                        servicedict['tsid'] = service.find('{foxtel:iq}tsid').text

                        resp['services'].append(servicedict)

                elif cmd=='planner_managment':

                    resp['error'] = "Not Yet implemented" #need to loop through services - not sure how to do that yet

                else:
                    resp['error'] = "Unknown command \'" + cmd + "\'."
            except: #failed to extract stanza
                resp['error'] = "Stanza received for \'" + cmd + "\' was a different structure to expected"


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
