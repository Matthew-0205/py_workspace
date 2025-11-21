#!/usr/bin/env python3

"""
  Copyright (c) 2021, SunSpec Alliance
  All Rights Reserved

"""

import json
import sys
import os
import time
import sunspec2.modbus.client as client
import sunspec2.file.client as file_client
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import pickle

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os

msg_id = 0

script_directory = os.path.dirname(os.path.realpath(__file__))
msg_id_file_name = os.path.join(script_directory, "pai_sunspec_msg_id.pkl")
if os.path.exists(msg_id_file_name):
    with open(msg_id_file_name, 'rb') as f:
        msg_id = pickle.load(f)
else:
    with open(msg_id_file_name, 'wb') as f:
        pickle.dump(msg_id, f) 
    
def sunspec_to_pai(sunspec: client.SunSpecModbusClientDeviceRTU) -> dict:
    pai_data = {}
    pai_data['ID'] = f'inverter{sunspec.slave_id}'
    pai_data['inverter_type'] = "sunspec"
    meters = []

    meter_count = 0
    for model in sunspec.model_list:
        a = (model.points.get('ID').cvalue)
        if model.points.get('ID').cvalue in [113]:
            meter = {}
            meter['meter_type'] = "AC"
            meter['ID'] = f'meter{meter_count + 1}'
            meter['phA_V'] = str(model.points.get('PhVphA').cvalue)
            meter['phB_V'] = str(model.points.get('PhVphB').cvalue)
            meter['phC_V'] = str(model.points.get('PhVphC').cvalue)
            meter['P'] = str(model.points.get('W').cvalue)
            meter['freq'] = str(model.points.get('Hz').cvalue)
            channels = []
            channel = {}
            channel['ID'] = 'ch1'
            channel['I'] = str(model.points.get('AphA').cvalue)
            channel['P'] = str(model.points.get('AphA').cvalue * model.points.get('PhVphA').cvalue)
            channel['pF'] = str(model.points.get('PF').cvalue)
            channel['KWh_In'] = str(model.points.get('WH').cvalue)
            channel['KWh_Out'] = 0
            channels.append(channel)
            
            channel = {}
            channel['ID'] = 'ch2'
            channel['I'] = str(model.points.get('AphB').cvalue)
            channel['P'] = str(model.points.get('AphB').cvalue * model.points.get('PhVphB').cvalue)
            channel['pF'] = str(model.points.get('PF').cvalue)
            channel['KWh_In'] = str(model.points.get('WH').cvalue)
            channel['KWh_Out'] = 0
            channels.append(channel)
            
            channel = {}
            channel['ID'] = 'ch3'
            channel['I'] = str(model.points.get('AphC').cvalue)
            channel['P'] = str(model.points.get('AphC').cvalue * model.points.get('PhVphC').cvalue)
            channel['pF'] = str(model.points.get('PF').cvalue)
            channel['KWh_In'] = str(model.points.get('WH').cvalue)
            channel['KWh_Out'] = 0
            
            channels.append(channel)
            
            meter['channels'] = channels
            
            meters.append(meter)
            meter_count += 1
        elif model.points.get('ID').cvalue == 160:
            {
                    "meter_type": "DC",
                    "ID": "meter2",
                    "phA_V": "618.200000",
                    "channels": [
                        {
                            "ID": "ch1",
                            "I": "13.800000",
                            "P": "8531.000000",
                            "KWh_In": "0",
                            "KWh_Out": "14414649"
                        }
                    ]
                },
            for group in model.groups['module']:
                meter = {}
                meter['meter_type'] = "DC"
                meter['ID'] = f'meter{meter_count + 1}'
                meter['phA_V'] = str(group.points.get('DCV').cvalue)
                meter['phA_V'] = str(group.points.get('DCV').cvalue)
                meter['phA_V'] = str(group.points.get('DCV').cvalue)
                channels = []
                channel = {}
                channel['ID'] = 'ch1'
                channel['I'] = str(group.points.get('DCA').cvalue)
                channel['P'] = str(group.points.get('DCA').cvalue * group.points.get('DCV').cvalue)
                channel['KWh_In'] = str(group.points.get('DCWH').cvalue)
                channel['KWh_Out'] = 0
                
                
            
                channels.append(channel)
            
                meter['channels'] = channels

                meters.append(meter)
                meter_count += 1
    pai_data['meters'] = meters
            
        
    # Map SunSpec data to PAI format
    # This is a placeholder for actual mapping logic
    return pai_data

script_dir = Path(__file__).parent.absolute()
print(script_dir)


endpoint = "a17kkqj3vtdek4-ats.iot.us-east-2.amazonaws.com"
root_ca_path = f"{script_dir}/aws_mqtt/ews_CA.pem"
certificate_path = f"{script_dir}/aws_mqtt/ews_cert.crt"
private_key_path = f"{script_dir}/aws_mqtt/ews-private.pem.key"
client_id = "pai_sunspec"
if __name__ == "__main__":
    
    
    mqtt_client = AWSIoTMQTTClient(client_id)
    mqtt_client.configureEndpoint(endpoint, 8883)
    mqtt_client.configureCredentials(root_ca_path, private_key_path, certificate_path)
     # Core connection configuration
    mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
    mqtt_client.configureOfflinePublishQueueing(-1)
    mqtt_client.configureDrainingFrequency(2)
    mqtt_client.configureConnectDisconnectTimeout(10)
    mqtt_client.configureMQTTOperationTimeout(5)
    
    mqtt_client.connect()
    # while(1):
    sunspec_devices = []
    
    for id in range(1, 2):
        try:
            sd = client.SunSpecModbusClientDeviceRTU(slave_id= id, name='/dev/ttyUSB0', baudrate=9600,parity=None, timeout=2.0)
            sd.scan()
            sunspec_devices.append(sd)
        except Exception as e:
            # print("Scan error: %s" % e)
            continue
    output = {}
    output["Version"] = "0.0.1"
    output['Timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    output["Timestamp_UTC"] = datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M:%S")
    output["DeviceID"] = "pai-s1"
    output["MsgID"] = f"0x{msg_id:04x}"
    output["Lat"] = "6.420000"
    output["Lng"] = "3.420000"
    output["RSSI"] = "0"
    output["VRC"] = [
    "0x0000000000000000",
    "0x0000000000000000",
    "0x0000000000000000",
    "0x0000000000000000"
]
    output["meters"] = []
    
    inverters = []
    for sd in sunspec_devices:
        inverters.append(sunspec_to_pai(sd))
    output['inverters'] = inverters
    
    mqtt_client.publish(f"psmv2/data", json.dumps(output), 1)
    
        # print(sd.models[160][0].groups['module'][0].points)
    print(json.dumps(output, indent=4))
    
    with open('sunspec_rtu_scan.json', 'w') as f:
        f.write(json.dumps(output))
    msg_id += 1
    with open(msg_id_file_name, 'wb') as f:
        pickle.dump(msg_id, f) 
            
    