
from sleekxmpp.xmlstream import ElementBase, ET

class error_reporting(ElementBase): # not working - dont think it's implemented

    namespace = "foxtel:iq"
    name = 'error_reporting'
    plugin_attrib = 'error_reporting'
    interfaces = set(('error_reporting','set_error','all_errors','get_error'))
    sub_interfaces = interfaces

class Hdd(ElementBase): #working for get
    namespace = 'foxtel:iq'
    name = 'hdd'
    plugin_attrib = 'hdd'
    interfaces = set(('temperature'))
    sub_interfaces = interfaces


class diagnostic_hdd(ElementBase): #working for get

    namespace = "foxtel:iq"
    name = 'diagnostic_hdd'
    plugin_attrib = 'diagnostic_hdd'
    interfaces = set(('reformat','error','temperature'))
    sub_interfaces = interfaces
    subitem = (Hdd,)

    def getTemperature(self):
        value=self['hdd'].xml.find('{foxtel:iq}temperature').text
        return value

class Tuner(ElementBase): #working

    namespace = "foxtel:iq"
    name = 'tuner'
    plugin_attrib = 'tuner'
    interfaces = set(('tuner_number','frequency','type','locked','quality'))
    sub_interfaces = interfaces

class diagnostic_tuner(ElementBase):  #working

    namespace = "foxtel:iq"
    name = 'diagnostic_tuner'
    plugin_attrib = 'diagnostic_tuner'
    interfaces = set(('tuners',))
    sub_interfaces = interfaces
    subitem = (Tuner,)


    def getTuners(self):
        tunerlist= []
        tuners=self.xml.findall('{foxtel:iq}tuner')
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

            tunerlist.append(tunerdict)
        return tunerlist


class Speed(ElementBase):

    namespace = "foxtel:iq"
    name = 'speed'
    plugin_attrib = 'speed'
    interfaces = set(('received','time'))
    sub_interfaces = interfaces

class diagnostic_speed_test(ElementBase): # not working

    namespace = "foxtel:iq"
    name = 'diagnostic_speed_test'
    plugin_attrib = 'diagnostic_speed_test'
    interfaces = set(('received','time','mbitspeed',))
    sub_interfaces = interfaces
    subitem = (Speed,)

    def getReceived(self):
        value=self['speed']['received']
        return value

    def getTime(self):
        value=self['speed']['time']
        return value

    def getMbitspeed(self):
        # size=self['speed'].xml.find('{foxtel:iq}received').text
        # time=self['speed'].xml.find('{foxtel:iq}time').text
        # speed = size / time / 1000
        return '5'#speed


class system_information(ElementBase): # working

    namespace = "foxtel:iq"
    name = 'system_information'
    plugin_attrib = 'system_information'
    interfaces = set(('manufacturer','hardware_version','software_version','serial_number','smartcard_number','fpn_firmware_version','epg_version'))
    sub_interfaces = interfaces

class volume(ElementBase): # working

    namespace = "foxtel:iq"
    name = 'volume'
    plugin_attrib = 'volume'
    interfaces = set(('current_volume','mute','response'))
    sub_interfaces = interfaces

class Broadcast(ElementBase): #working
    namespace = 'foxtel:iq'
    name = 'broadcast'
    plugin_attrib = 'broadcast'
    interfaces = set(('type','lcn','onid','tsid','svcid','servicekey','name'))
    sub_interfaces = interfaces

class current_viewing(ElementBase): #working - only tested for broadcast
    namespace = "foxtel:iq"
    name = 'current_viewing'
    plugin_attrib = 'current_viewing'
    interfaces = set(('type','lcn','onid','tsid','svcid','servicekey','name','current_channel','response','error'))
    sub_interfaces = interfaces
    subitem = (Broadcast,)

    def getType(self):
        value=self['broadcast']['type']
        return value

    def getLcn(self):
        value=self['broadcast']['lcn']
        return value

    def getOnid(self):
        value=self['broadcast']['onid']
        return value

    def getTsid(self):
        value=self['broadcast']['tsid']
        return value

    def getSvcid(self):
        value=self['broadcast']['svcid']
        return value

    def getServicekey(self):
        value=self['broadcast']['servicekey']
        return value

    def getName(self):
        value=self['broadcast']['name']
        return value

class Programme(ElementBase): #working
    namespace = 'foxtel:iq'
    name = 'programme'
    plugin_attrib = 'programme'
    interfaces = set(('event_name', 'start_time','event_length','synopsys','genre','rating'))
    sub_interfaces = interfaces

class current_programme(ElementBase): # working
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
    interfaces = set(('response',))
    sub_interfaces = interfaces

class reboot_stb(ElementBase):
    namespace = "foxtel:iq"
    name = 'reboot_stb'
    plugin_attrib = 'reboot_stb'
    interfaces = set(('response',))
    sub_interfaces = interfaces

#needs a hash value... not sure how this works
class code_download(ElementBase):
    namespace = "foxtel:iq"
    name = 'code_download'
    plugin_attrib = 'code_download'
    interfaces = set(('response','background','url'))
    sub_interfaces = interfaces

class stb_model(ElementBase): # working - but box returned a blank
    namespace = "foxtel:iq"
    name = 'stb_model'
    plugin_attrib = 'stb_model'
    interfaces = set(('stb_model',))
    sub_interfaces = interfaces

class dvbt_services(ElementBase): # box doesnt have FTA connected so cant test
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


class planner(ElementBase): # working
    namespace = "foxtel:iq"
    name = 'planner'
    plugin_attrib = 'planner'
    interfaces = set(('start','qty','items','end'))
    sub_interfaces = set(('items'))

    def getItems(self):
        itemslist= []
        items=self.xml.findall('{foxtel:iq}item')
        for item in items:
            itemdict={}
            itemdict['dur'] = item.find('{foxtel:iq}dur').text
            itemdict['evt_desc'] = item.find('{foxtel:iq}evt_desc').text
            itemdict['evt_name'] = item.find('{foxtel:iq}evt_name').text
            itemdict['file_exp'] = item.find('{foxtel:iq}file_exp').text
            itemdict['genre'] = item.find('{foxtel:iq}genre').text
            itemdict['keep'] = item.find('{foxtel:iq}keep').text
            itemdict['prog_id'] = item.find('{foxtel:iq}prog_id').text
            itemdict['rating'] = item.find('{foxtel:iq}rating').text
            itemdict['rec_rem_dl'] = item.find('{foxtel:iq}rec_rem_dl').text
            itemdict['start_time'] = item.find('{foxtel:iq}start_time').text
            itemdict['state'] = item.find('{foxtel:iq}state').text
            itemdict['viewed'] = item.find('{foxtel:iq}viewed').text

            itemslist.append(itemdict)
        return itemslist



#pushvod goes here - same as above


#stopped halfway through this - not sure if it works or the value
class epg_managment(ElementBase):
    namespace = "foxtel:iq"
    name = 'epg_managment'
    plugin_attrib = 'epg_managment'
    interfaces = set(('epg_managment','setting','video_output','video_hdoutput','video_aspect','video_tvtype','video_16x9','video_wss','video_4x3','video_cc''audio_language','audio_output','audio_spdif','audio_delay','audio_hdmi','tvguide_adultfilter','tvguide_reminder','tvguide_colour','tvguide_video',''))
    sub_interfaces = interfaces

class key_value_pair(ElementBase): # working
    namespace = "foxtel:iq"
    name = 'key_value_pair'
    plugin_attrib = 'key_value_pair'
    interfaces = set(('all','key','pairs'))
    sub_interfaces = set(('key','pairs'))

    def getPairs(self):
        kvpsdict= {}
        kvps=self.xml.findall('{foxtel:iq}pair')
        for kvp in kvps:
            key = kvp.find('{foxtel:iq}key').text
            try:
                kvpsdict[key]=kvp.find('{foxtel:iq}value').text
            except:
                try:
                    kvpsdict['error']=kvp.find('{foxtel:iq}error').text
                except:
                    kvpsdict['error']='Unknown Error'

        return kvpsdict

#popup message goes here - not included as does not work!

#logging sanzas go here - too long and complicted for now
