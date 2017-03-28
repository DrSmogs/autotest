
from sleekxmpp.xmlstream import ElementBase, ET

# <iq type="set">
#   <task id="123" xmlns="example:task">
#     <command>python script.py</command>
#     <cleanup>rm temp.txt</cleanup>
#     <param>
#       <name>foo</name>
#       <value>fizz</value>
#     </param>
#     <param>
#       <name>bar</name>
#       <value>buzz</value>
#     </param>
#   </task>
# </iq>


# class Param(ElementBase):
#     namespace = 'example:task'
#     name = 'param'
#     plugin_attrib = 'param'
#     interfaces = set(('name', 'value'))
#     sub_interfaces = interfaces
#
# class Task(ElementBase):
#     namespace = 'example:task'
#     name = 'task'
#     plugin_attrib = 'task'
#     interfaces = set(('id', 'command', 'cleanup', 'params'))
#     sub_interfaces = set(('command', 'cleanup'))
#     subitem = (Param,)
#
#     def getParams(self):
#         params = {}
#         for par in self.xml.findall('{%s}param' % Param.namespace):
#             param = Param(par)
#             params[param['name']] = param['value']
#         return params
#
#     def setParams(self, params):
#         # params is a dictonary
#         for name in params:
#             self.addParam(name, params[name])
#
#     def delParams(self):
#         params = self.xml.findall('{%s}param' % Param.namespace)
#         for param in params:
#             self.xml.remove(param)
#
#     def addParam(self, name, value):
#         # Use Param(None, self) to link the param object
#         # with the task object.
#         param_obj = Param(None, self)
#         param_obj['name'] = name
#         param_obj['value'] = value
#
#     def delParam(self, name):
#         # Get all <param /> elements
#         params = self.xml.findall('{%s}param' % Param.namespace)
#         for parXML in params:
#             # Create a stanza object to test against
#             param = Param(parXML)
#             # Remove <param /> element if name matches
#             if param['name'] == name:
#                 self.xml.remove(parXML)






class error_reporting(ElementBase):

    namespace = "foxtel:iq"
    name = 'error_reporting'
    plugin_attrib = 'error_reporting'
    interfaces = set(('error_reporting','set_error','all_errors','get_error'))
    sub_interfaces = interfaces

class diagnostic_hdd(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_hdd'
    plugin_attrib = 'diagnostic_hdd'
    interfaces = set(('diagnostic_hdd','hdd','reformat'))
    sub_interfaces = interfaces


class diagnostic_tuner(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_tuner'
    plugin_attrib = 'diagnostic_tuner'
    interfaces = set(('diagnostic_tuner'))
    sub_interfaces = interfaces


class diagnostic_speed_test(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_speed_test'
    plugin_attrib = 'diagnostic_speed_test'
    interfaces = set(('diagnostic_speed_test'))
    sub_interfaces = interfaces

class system_information(ElementBase):

    namespace = "foxtel:iq"
    name = 'system_information'
    plugin_attrib = 'system_information'
    interfaces = set(('system_information'))
    sub_interfaces = interfaces

class volume(ElementBase):

    namespace = "foxtel:iq"
    name = 'volume'
    plugin_attrib = 'volume'
    interfaces = set(('volume','current_volume','mute'))
    sub_interfaces = interfaces

class current_viewing(ElementBase):
    namespace = "foxtel:iq"
    name = 'current_viewing'
    plugin_attrib = 'current_viewing'
    interfaces = set(('current_viewing','current_channel'))
    sub_interfaces = interfaces

class current_programme(ElementBase):
    namespace = "foxtel:iq"
    name = 'current_programme'
    plugin_attrib = 'current_programme'
    interfaces = set(('current_programme','programme'))
    sub_interfaces = interfaces


#this is not correct but will come back to it
class remote_control(ElementBase):
    namespace = "foxtel:iq"
    name = 'remote_control'
    plugin_attrib = 'remote_control'
    interfaces = set(('remote_control','stop_any_script', 'ignore_external_rcu','acknowledge_immediately','ignore_external_front_panel','button_key'))
    sub_interfaces = interfaces

    def get_button_key(self):
        button = self.xml.find('{%s}button_key' % self.namespace)
        if button is not None:
            return button.attrib.get('path', '')
        return path

    def set_button_key(self, value):
        self.del_metadata()
        if value:
            button = ET.Element('{%s}button_key' % self.namepace)
            button.attrib['path'] = value
            self.xml.append(meta)

    def del_button_key(self):
        button = self.xml.find('{%s}button_key' % self.namespace)
        if button is not None:
            self.xml.remove(button)


class reset_pin(ElementBase):
    namespace = "foxtel:iq"
    name = 'reset_pin'
    plugin_attrib = 'reset_pin'
    interfaces = set(('reset_pin'))
    sub_interfaces = interfaces

class reboot_stb(ElementBase):
    namespace = "foxtel:iq"
    name = 'reboot_stb'
    plugin_attrib = 'reboot_stb'
    interfaces = set(('reboot_stb'))
    sub_interfaces = interfaces

#needs a hash value... not sure how this works
class code_download(ElementBase):
    namespace = "foxtel:iq"
    name = 'code_download'
    plugin_attrib = 'code_download'
    interfaces = set(('code_download','background','url'))
    sub_interfaces = interfaces

class stb_model(ElementBase):
    namespace = "foxtel:iq"
    name = 'stb_model'
    plugin_attrib = 'stb_model'
    interfaces = set(('stb_model'))
    sub_interfaces = interfaces

class dvbt_services(ElementBase):
    namespace = "foxtel:iq"
    name = 'dvbt_services'
    plugin_attrib = 'dvbt_services'
    interfaces = set(('dvbt_services','service'))
    sub_interfaces = interfaces

#requires a substanza - not sure how to implement this yet
class Event(ElementBase):
    namespace = 'foxtel:iq'
    name = 'event'
    plugin_attrib = 'event'
    interfaces = set(('event_id', 'onid','tsid','svcid','freq','svl_entry','start_time','end_time','series_link','extend','keep','rec_rem'))
    sub_interfaces = interfaces

#not sure how to do this....
class remote_booking(ElementBase):
    namespace = "foxtel:iq"
    name = 'remote_booking'
    plugin_attrib = 'remote_booking'
    interfaces = set(('remote_booking','events'))
    sub_interfaces = interfaces
    subitem = (Event,)

    def getEvents(self):
        events = {}
        for evt in self.xml.findall('{%s}event' % Event.namespace):
            event = Event(evt)
            events[event[evt]] = param[evt]
        return params

    def setEvents(self, events):
        # events is a dictonary
        for name in params:
            self.addEvent(name, events[name])

    def delEvents(self):
        events = self.xml.findall('{%s}event' % Event.namespace)
        for event in events:
            self.xml.remove(event)

    def addEvent(self, name, value):
        # Use Param(None, self) to link the param object
        # with the task object.
        param_obj = Event(None, self)
        param_obj['name'] = name
        param_obj['value'] = value

    def delEvent(self, name):
        # Get all <param /> elements
        events = self.xml.findall('{%s}event' % Event.namespace)
        for parXML in events:
            # Create a stanza object to test against
            event = Event(parXML)
            # Remove <param /> element if name matches
            if event['name'] == name:
                self.xml.remove(parXML)


#planner manager goes here - wait until i understand remote_booking first.

#pushvod goes here - same as above


#stopped halfway through this - not sure if it works or the value
class epg_managment(ElementBase):
    namespace = "foxtel:iq"
    name = 'epg_managment'
    plugin_attrib = 'epg_managment'
    interfaces = set(('epg_managment','setting','video_output','video_hdoutput','video_aspect','video_tvtype','video_16x9','video_wss','video_4x3','video_cc''audio_language','audio_output','audio_spdif','audio_delay','audio_hdmi','tvguide_adultfilter','tvguide_reminder','tvguide_colour','tvguide_video',''))
    sub_interfaces = interfaces

#kjey value pairs goes here - too long and complicated

#popup message goes here - not included as does not work!

#logging sanzas go here - too long and complicted for now
