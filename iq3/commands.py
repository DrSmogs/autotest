import logging

import time

from sleekxmpp.stanza import StreamFeatures, Iq
from sleekxmpp.xmlstream import register_stanza_plugin, JID
from sleekxmpp.plugins import BasePlugin

from iq3 import stanza, error_reporting, diagnostic_hdd, diagnostic_tuner, diagnostic_speed_test, system_information, volume, current_viewing
from iq3 import current_programme, remote_control, reset_pin, reboot_stb, code_download, stb_model, dvbt_services, remote_booking, epg_managment

from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher.id import MatcherId
import xml.etree.ElementTree as ET


class iq3(BasePlugin):

    name = 'iq3'
    description = 'my iq3'

    def plugin_init(self):
        register_stanza_plugin(Iq, error_reporting)
        register_stanza_plugin(Iq, diagnostic_hdd)
        register_stanza_plugin(Iq, diagnostic_tuner)
        register_stanza_plugin(Iq, diagnostic_speed_test)
        register_stanza_plugin(Iq, system_information)
        register_stanza_plugin(Iq, volume)
        register_stanza_plugin(Iq, current_viewing)
        register_stanza_plugin(Iq, current_programme)
        register_stanza_plugin(Iq, remote_control)
        register_stanza_plugin(Iq, reset_pin)
        register_stanza_plugin(Iq, reboot_stb)
        register_stanza_plugin(Iq, code_download)
        register_stanza_plugin(Iq, stb_model)
        register_stanza_plugin(Iq, dvbt_services)
        register_stanza_plugin(Iq, remote_booking)
        register_stanza_plugin(Iq, epg_managment)

        self.sessions = {};

    def get_cmd(self, cmd=None, jid=None, tjid=None, resource='iq3'):
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = tjid + "-" + str(int(time.time()))
        iq['xml:lang'] = 'en'
        iq['type'] = 'get'
        if cmd=='error_reporting':
            iq['error_reporting']['get_error']='reboot'
        iq.enable(cmd)

        resp = iq.send(block=True)

        return resp







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
