
from sleekxmpp.xmlstream import ElementBase, ET

class error_reporting(ElementBase):

    namespace = "foxtel:iq"
    name = 'error_reporting'
    plugin_attrib = 'error_reporting'
    interfaces = set(('error_reporting','set_error','all_errors','get_error'))
    sub_interfaces = interfaces

class Hdd(ElementBase):
    namespace = 'foxtel:iq'
    name = 'hdd'
    plugin_attrib = 'hdd'
    interfaces = set(('temperature'))
    sub_interfaces = interfaces


class diagnostic_hdd(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_hdd'
    plugin_attrib = 'diagnostic_hdd'
    interfaces = set(('reformat','error'))
    sub_interfaces = interfaces,
    subitem = (Hdd,)


class diagnostic_tuner(ElementBase): #needs to be updated for sub stuff

    namespace = "foxtel:iq"
    name = 'diagnostic_tuner'
    plugin_attrib = 'diagnostic_tuner'
    interfaces = set(('diagnostic_tuner'))
    sub_interfaces = interfaces

class Speed(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_speed_test'
    plugin_attrib = 'diagnostic_speed_test'
    interfaces = set(('received','time'))
    sub_interfaces = interfaces

class diagnostic_speed_test(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_speed_test'
    plugin_attrib = 'diagnostic_speed_test'
    interfaces = set(())
    sub_interfaces = interfaces
    subitem = (Speed,)

class system_information(ElementBase):

    namespace = "foxtel:iq"
    name = 'system_information'
    plugin_attrib = 'system_information'
    interfaces = set(('manufacturer','hardware_version','software_version','serial_number','smartcard_number','fpn_firmware_version','epg_version'))
    sub_interfaces = interfaces

class volume(ElementBase):

    namespace = "foxtel:iq"
    name = 'volume'
    plugin_attrib = 'volume'
    interfaces = set(('current_volume','mute'))
    sub_interfaces = interfaces

class current_viewing(ElementBase):
    namespace = "foxtel:iq"
    name = 'current_viewing'
    plugin_attrib = 'current_viewing'
    interfaces = set(('type','lcn','onid','tsid','svcid','servicekey','name'))
    sub_interfaces = interfaces

class Programme(ElementBase):
    namespace = 'foxtel:iq'
    name = 'programme'
    plugin_attrib = 'programme'
    interfaces = set(('event_name', 'start_time','event_length','synopsys','genre','rating'))
    sub_interfaces = interfaces



class current_programme(ElementBase): # needs sub stuff
    namespace = "foxtel:iq"
    name = 'current_programme'
    plugin_attrib = 'current_programme'
    interfaces = set(('event_name','start_time','event_length','synopsys','genre','rating'))
    sub_interfaces = interfaces
    subitem = (Programme,)

    def getEvent_Name(self):
        value=self['programme']['event_name']
        return value

    def getStart_Time(self):
        value=self['programme']['start_time']
        return value

    def getEvent_Length(self):
        value=self['programme']['event_length']
        return value

    def getSynopsys(self):
        value=self['programme']['synopsys']
        return value
    def getGenre(self):
        value=self['programme']['genre']
        return value

    def getRating(self):
        value=self['programme']['rating']
        return value

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

class dvbt_services(ElementBase): # needs sub stuff
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


# planner needs sub items - not sure how to do that yet...
class planner(ElementBase):
    namespace = "foxtel:iq"
    name = 'planner'
    plugin_attrib = 'planner'
    interfaces = set(('start','qty','item'))
    sub_interfaces = set(('item'))

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
