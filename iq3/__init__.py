from sleekxmpp.plugins.base import register_plugin, BasePlugin

from iq3.stanza import error_reporting, diagnostic_hdd, Hdd, diagnostic_tuner, Tuner, diagnostic_speed_test, Speed
from iq3.stanza import current_programme, Programme, remote_control, reset_pin, reboot_stb, code_download, stb_model, dvbt_services, remote_booking, epg_managment
from iq3.stanza import planner, system_information, volume, current_viewing, Broadcast, key_value_pair

from iq3.commands import iq3



register_plugin(iq3)
