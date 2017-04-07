import logging

import time

from sleekxmpp.stanza import StreamFeatures, Iq
from sleekxmpp.xmlstream import register_stanza_plugin, JID
from sleekxmpp.plugins import BasePlugin

from iq3 import stanza, error_reporting, diagnostic_hdd, Hdd, diagnostic_tuner, diagnostic_speed_test, Speed, system_information, volume, current_viewing
from iq3 import current_programme, Programme, remote_control, reset_pin, reboot_stb, code_download, stb_model, dvbt_services, remote_booking, epg_managment
from iq3 import planner
from iq3.resp import iq3resp

from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback
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
        register_stanza_plugin(Iq, diagnostic_speed_test)
        register_stanza_plugin(diagnostic_speed_test,Speed, iterable=True)
        register_stanza_plugin(Iq, system_information)
        register_stanza_plugin(Iq, volume)
        register_stanza_plugin(Iq, current_viewing)
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


    def get_cmd(self, cmd=None, boxes=None, jid=None, tjid=None, resource='iq3'):
        self.responses=0
        self.boxes=boxes
        timeout = config.reqtimeout
        period = 0.25
        starttime = time.time()
        endtime = starttime + timeout
        self.results = []
        self.replies={}
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
                print(iq['error'])
                print(iq['error'].keys())

            else:
                stanza=next(iter(iq.loaded_plugins))
                for key in iq[stanza].keys():
                    if key not in ('lang', 'substanzas','programme'):
                        result[key]=iq[stanza][key]

            # print(iq[stanza].keys())
            # print(iq[stanza]['event_name'])
            # result='hello'
            # print(result)
            self.results.append(result)


        for box in boxes:

            iq = self.xmpp.Iq()
            iq['from'] = jid + "/" + resource
            iq['to'] = box+config.boxloginpart+'@'+config.xmppdomain + "/" + resource
            iq['id'] = box + "-" + str(int(time.time()))
            iq['xml:lang'] = 'en'
            iq['type'] = 'get'
            if cmd=='planner':
                iq['planner']['start'] = '0'
                iq['planner']['qty'] = '5'

            iq.enable(cmd)
            cb_name = iq.send(callback=iq3_cb)

        while time.time() < endtime:
            if self.responses==len(boxes):
                print("I have received all the responses!")
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
        return self.results


    def set_viewing(self, jid=None, tjid=None, resource=None, chan=None):
        seqnr = "1234567"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'set'
        iq['xml:lang'] = 'en'
        iq['current_viewing']['current_channel'] = chan
        iq.enable('current_viewing')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_viewing", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp
