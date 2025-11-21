#!/usr/bin/env python3

"""
  Copyright (c) 2021, SunSpec Alliance
  All Rights Reserved

"""
import pickle
import time
import sunspec2.modbus.client as client
from optparse import OptionParser
import json


usage = 'usage: %prog [options]'
parser = OptionParser(usage=usage)
parser.add_option('-a', metavar=' ', type='int',
                  default=1,
                  help='modbus slave address [default: 1]')
options, args = parser.parse_args()

addr = options.a
pickle_file_name = f"/home/pai/Documents/sunspec_pai/pysunspec2/data_inverter_readings_{addr}.pkl"
save_file_name = f"/home/pai/Documents/sunspec_pai/pysunspec2/inverter_readings_{addr}.json"





loaded_data = {}
try:
  with open(pickle_file_name, "rb") as f:
      loaded_data = pickle.load(f)
except:
  loaded_data = {"DeviceID": f"pai-Matthew_{addr}",
          "MsgID": 0,
          "Lat": "6.340000", 
          "Lng": "3.420000",}

  with open(pickle_file_name, "wb") as f:
      pickle.dump(loaded_data, f)

def getFroniusData(slave_id):
  sd = client.SunSpecModbusClientDeviceRTU(slave_id=slave_id, name="/dev/ttyUSB0", baudrate=9600,
                                                      parity=None, timeout=1)
  if sd is not None:
      # read all models in the device
      sd.scan()
      
      inverter = sd.inverter_three_phase_float[0]
      mppt = sd.mppt[0]
      sd.disconnect()
      sd.close()
      return {
         "inverter": inverter.get_dict(),
          "mppt": mppt.get_dict(),
      }



loaded_data["MsgID"] += 1
dic = {"Timestamp" : time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()),
      "DeviceID" : loaded_data["DeviceID"],
      "MsgID" : loaded_data["MsgID"],
      "Lat" : loaded_data["Lat"],
      "Lng" : loaded_data["Lng"],
      "inverter" : getFroniusData(slave_id = addr)
}



with open(save_file_name, "a") as f:
  f.write("\n\n"+ json.dumps(dic))
  
with open(pickle_file_name, "wb") as f:
  pickle.dump(loaded_data, f)


