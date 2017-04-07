def iq3resp(iq):

    if 'error' in iq.loaded_plugins:
        stanza='error'
    else:
        stanza=next(iter(iq.loaded_plugins))
    print(iq[stanza].keys())
    print(iq[stanza]['event_name'])

    # dict={}
    #
    # if stanza == 'error_reporting':
    #
    #     dict['error'] = "error_reporting not implemented"
    #
    # elif stanza== 'diagnostic_hdd':
    #     dict['temperature'] = iq[stanza]['hdd']['temperature']

    # elif stanza=='diagnostic_tuner':
    #     dict['tuners'] = []
    #     tuners=resp.xml.findall('{foxtel:iq}diagnostic_tuner/{foxtel:iq}tuner')
    #     for tuner in tuners:
    #         tunerdict={}
    #         tunerdict['tuner_number'] = tuner.find('{foxtel:iq}tuner_number').text
    #         tunerdict['frequency'] = tuner.find('{foxtel:iq}frequency').text
    #         tunerdict['type'] = tuner.find('{foxtel:iq}type').text
    #         tunerdict['locked'] = tuner.find('{foxtel:iq}locked').text
    #         try:
    #             tunerdict['level_dBm'] = tuner.find('{foxtel:iq}level').text
    #             quality = tuner.findall('{foxtel:iq}quality')
    #
    #         except:
    #             tunerdict['level_dBm'] = 'N/A'
    #             tunerdict['quality_snr_db'] = 'N/A'
    #             tunerdict['quality_uncorrected_ber'] = 'N/A'
    #
    #         else:
    #             for qual in quality:
    #
    #                 if qual.attrib['type']=="signal_to_noise":
    #                     tunerdict['quality_snr_db'] = qual.text
    #
    #                 elif qual.attrib['type']=="uncorrected_BER":
    #                     tunerdict['quality_uncorrected_ber'] = qual.text
    #
    #                 elif qual.attrib['type']=="corrected_BER":
    #                     tunerdict['quality_corrected_ber'] = qual.text
    #
    #         dict['tuners'].append(tunerdict)

    # elif stanza=='diagnostic_speed_test':
    #     dict['received'] = iq[stanza]['speed_test']['received']
    #     dict['time'] = iq[stanza]['speed_test']['time']
    #
    # elif stanza=='system_information':
    #     dict['manufacturer'] = iq[stanza]['speed_test']
    #     dict['hardware_version'] = resp.xml.find('{foxtel:iq}system_information/{foxtel:iq}hardware_version').text
    #     dict['software_version'] = resp.xml.find('{foxtel:iq}system_information/{foxtel:iq}software_version').text
    #     dict['serial_number'] = resp.xml.find('{foxtel:iq}system_information/{foxtel:iq}serial_number').text
    #     dict['smartcard_number'] = resp.xml.find('{foxtel:iq}system_information/{foxtel:iq}smartcard_number').text
    #     dict['fpn_firmware_version'] = resp.xml.find('{foxtel:iq}system_information/{foxtel:iq}fpn_firmware_version').text
    #     dict['epg_version'] = resp.xml.find('{foxtel:iq}system_information/{foxtel:iq}epg_version').text
    #
    # elif stanza=='volume':
    #     dict['current_volume'] = resp.xml.find('{foxtel:iq}volume/{foxtel:iq}current_volume').text
    #     dict['mute'] = resp.xml.find('{foxtel:iq}volume/{foxtel:iq}mute').text
    #
    # elif stanza=='current_viewing': #need to add in variants for recording and ip.. only braodcast below
    #     dict['type'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}type').text
    #     dict['lcn'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}lcn').text
    #     dict['onid'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}onid').text
    #     dict['tsid'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}tsid').text
    #     dict['svcid'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}svcid').text
    #     dict['servicekey'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}servicekey').text
    #     dict['name'] = resp.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}broadcast/{foxtel:iq}name').text
    #
    # elif stanza=='current_programme':
    #     dict['event_name'] = resp.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
    #     dict['start_time'] = resp.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
    #     dict['event_length'] = resp.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
    #     dict['synopsys'] = resp.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
    #     dict['genre'] = resp.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
    #     dict['parental_rating'] = resp.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text
    #
    # elif stanza=='stb_model':
    #     dict['model'] = resp.xml.find('{foxtel:iq}stb_model/{foxtel:iq}model').text #This works in the API - but not working on the box
    #
    # elif stanza=='dvbt_services':
    #     dict['services'] = []
    #     services=resp.xml.findall('{foxtel:iq}dvbt_services/{foxtel:iq}service')
    #     for service in services:
    #         servicedict={}
    #         servicedict['onid'] = service.find('{foxtel:iq}onid').text
    #         servicedict['service_key'] = service.find('{foxtel:iq}service_key').text
    #         servicedict['svc_name'] = service.find('{foxtel:iq}svc_name').text
    #         servicedict['svcid'] = service.find('{foxtel:iq}svcid').text
    #         servicedict['tsid'] = service.find('{foxtel:iq}tsid').text
    #
    #         dict['services'].append(servicedict)
    #
    # elif stanza=='planner':
    #     dict['items'] = []
    #     items=resp.xml.findall('{foxtel:iq}planner/{foxtel:iq}item')
    #
    #     for item in items:
    #         itemsdict={}
    #         itemsdict['prog_id'] = item.find('{foxtel:iq}prog_id').text
    #         itemsdict['evt_name'] = item.find('{foxtel:iq}evt_name').text
    #         itemsdict['evt_desc'] = item.find('{foxtel:iq}evt_desc').text
    #         itemsdict['genre'] = item.find('{foxtel:iq}genre').text
    #         itemsdict['rating'] = item.find('{foxtel:iq}rating').text
    #         itemsdict['rec_rem_dl'] = item.find('{foxtel:iq}rec_rem_dl').text
    #         itemsdict['state'] = item.find('{foxtel:iq}state').text
    #         itemsdict['keep'] = item.find('{foxtel:iq}keep').text
    #         itemsdict['start_time'] = item.find('{foxtel:iq}start_time').text
    #         itemsdict['file_exp'] = item.find('{foxtel:iq}file_exp').text
    #         itemsdict['dur'] = item.find('{foxtel:iq}dur').text
    #         itemsdict['viewed'] = item.find('{foxtel:iq}viewed').text
    #     #     itemsdict['s_link'] = item.find('{foxtel:iq}s_link').text
    #     #     itemsdict['extend'] = item.find('{foxtel:iq}extend').text
    #     #     itemsdict['error_flags'] = item.find('{foxtel:iq}error_flags').text
    #
    #     # tree = ET.parse(out)
    #     # root = tree.getroot()
    #     # print("this is root")
    #     # print(root.attrib)
    #     # dict['TEST']=root.attrib
    #
    #     dict['items'].append(itemsdict)
    # else:
    #     dict['error'] = "Unknown command \'" + stanza + "\'."
    #
    #
    # return dict
