import logging

import time

from sleekxmpp.stanza import StreamFeatures, Iq
from sleekxmpp.xmlstream import register_stanza_plugin, JID
from sleekxmpp.plugins import BasePlugin

from iq3 import stanza, error_reporting, diagnostic_hdd, Hdd, diagnostic_tuner, Tuner, diagnostic_speed_test, Speed
from iq3 import current_programme, Programme, remote_control, reset_pin, reboot_stb, code_download, stb_model, dvbt_services, remote_booking, epg_managment
from iq3 import planner, system_information, volume, current_viewing, Broadcast, key_value_pair


from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.handler import *
from sleekxmpp.xmlstream.matcher.id import MatcherId
from sleekxmpp.xmlstream.matcher import MatchXPath
import xml.etree.ElementTree as ET

from config import config


class iq3(BasePlugin):

    name = 'iq3'
    description = 'my iq3'


    def plugin_init(self):


        register_stanza_plugin(Iq, error_reporting)
        register_stanza_plugin(Iq, diagnostic_hdd)
        register_stanza_plugin(diagnostic_hdd,Hdd, iterable=True)
        register_stanza_plugin(Iq, diagnostic_tuner)
        register_stanza_plugin(diagnostic_tuner,Tuner, iterable=True)
        register_stanza_plugin(Iq, diagnostic_speed_test)
        register_stanza_plugin(diagnostic_speed_test,Speed, iterable=True)
        register_stanza_plugin(Iq, system_information)
        register_stanza_plugin(Iq, volume)
        register_stanza_plugin(Iq, current_viewing)
        register_stanza_plugin(current_viewing,Broadcast, iterable=True)
        register_stanza_plugin(Iq, current_programme)
        register_stanza_plugin(current_programme,Programme, iterable=True)
        register_stanza_plugin(Iq, remote_control)
        register_stanza_plugin(Iq, reset_pin)
        register_stanza_plugin(Iq, reboot_stb)
        register_stanza_plugin(Iq, code_download)
        register_stanza_plugin(Iq, stb_model)
        register_stanza_plugin(Iq, dvbt_services)
        register_stanza_plugin(Iq, remote_booking)
        register_stanza_plugin(Iq, epg_managment)
        register_stanza_plugin(Iq, planner)
        register_stanza_plugin(Iq, key_value_pair)

    def iq3_cmd(self,request='get', cmd=None, boxes=None, jid=None, tjid=None, resource='iq3',timeout=None,params=None):
        self.testparam_start = 0
        self.testparam_qty = 5
        self.responses=0
        self.boxes=boxes
        period = 0.25
        starttime = time.time()
        endtime = starttime + timeout
        self.results = []
        self.replies=[]
        self.callbacks=[]
        def iq3_cb(iq):
            self.responses =self.responses+1
            print("Recieved " + str(self.responses) + " out of " +str(len(self.boxes)) + " messages sent!")
            result={}
            boxid=str(iq['from'])
            boxid = boxid.split('.')[0]
            boxid = boxid.split('@')[0]
            result['box_id'] = boxid
            self.replies.append(boxid)
            if 'error' in iq.loaded_plugins:
                stanza='error'
                result['error_type']=iq['error']['type']
                result['error_text']=iq['error']['text']
                result['error_condition']=iq['error']['condition']


            else:
                stanza=next(iter(iq.loaded_plugins))
                print("debug time !!!!!!!!!!!!!!!!!!!!")
                print(iq[stanza].keys())
                for key in iq[stanza].keys():
                    if key not in ('lang', 'substanzas'):
                        if isinstance(iq[stanza][key],(str,dict,list)):
                            if iq[stanza][key] =="":
                                None
                            else:
                                result[key]=iq[stanza][key]

            self.results.append(result)


        for box in boxes:

            iq = self.xmpp.Iq()
            iq['from'] = jid + "/" + resource
            iq['to'] = box+config.boxloginpart+'@'+config.xmppdomain + "/" + resource
            iq['id'] = box + "-" + str(int(time.time()))
            iq['xml:lang'] = 'en'
            iq['type'] = request
            for key in params.keys():
                iq[cmd][key] = params[key]

            iq.enable(cmd)
            cb_name = iq.send(callback=iq3_cb)
            self.callbacks.append(cb_name)

        while time.time() < endtime:
            if self.responses==len(boxes):
                print("I have received all the responses!")

                for callback in self.callbacks: #Remove any callbackls generated
                    print(callback + " removed")
                    self.xmpp.remove_handler(cb_name)
                return self.results
            else:
                time.sleep(period)
        print("timeout reached")
        for box in boxes:
            result = {}

            if box not in self.replies:
                result['box_id'] = box
                result['error'] = 'This box timed out after ' + str(timeout) + ' seconds'
                self.results.append(result)

                for callback in self.callbacks: #Remove any callbackls generated
                    print(callback + " removed")
                    self.xmpp.remove_handler(cb_name)
        return self.results
