from datetime import datetime
import os
from typing import List
from pymodbus.client import ModbusSerialClient
# from modbus_utils import *
import struct
import time 


class PD194z:
    fields_to_addr = {
    "PHASE_A_VOLTAGE"        : 0x06,
    "PHASE_B_VOLTAGE"        : 0x08,
    "PHASE_C_VOLTAGE"        : 0x0A,
    "LINE_A_B_VOLTAGE"       : 0x0C,
    "LINE_B_C_VOLTAGE"       : 0x0E,
    "LINE_C_A_VOLTAGE"       : 0x10,
    "FREQ_HZ"                : 0x12,
    # ////////////////////////////////////
    "CCT_1_PHASE_A_CURRENT"  : 0x14,
    "CCT_1_PHASE_B_CURRENT"  : 0x16,
    "CCT_1_PHASE_C_CURRENT"  : 0x18,
    "CCT_1_NEUTRAL_CURRENT"  : 0x1A,
    "CCT_1_PHASE_A_PWR"      : 0x1C,
    "CCT_1_PHASE_B_PWR"      : 0x1E,
    "CCT_1_PHASE_C_PWR"      : 0x20,
    "CCT_1_TOTAL_PWR"        : 0x22,
    "CCT_1_PHASE_A_PF"       : 0x34,
    "CCT_1_PHASE_B_PF"       : 0x36,
    "CCT_1_PHASE_C_PF"       : 0x38,
    "CCT_1_PHASE_A_KWH_OUT"  : 0x3C,
    "CCT_1_PHASE_B_KWH_OUT"  : 0x3E,
    "CCT_1_PHASE_C_KWH_OUT"  : 0x40,
    "CCT_1_PHASE_A_KWH_IN"   : 0x44,
    "CCT_1_PHASE_B_KWH_IN"   : 0x46,
    "CCT_1_PHASE_C_KWH_IN"   : 0x48,
    # ////////////////////////////////////
    "CCT_2_PHASE_A_CURRENT"  : 0x5C,
    "CCT_2_PHASE_B_CURRENT"  : 0x5E,
    "CCT_2_PHASE_C_CURRENT"  : 0x60,
    "CCT_2_NEUTRAL_CURRENT"  : 0x62,
    "CCT_2_PHASE_A_PWR"      : 0x64,
    "CCT_2_PHASE_B_PWR"      : 0x66,
    "CCT_2_PHASE_C_PWR"      : 0x68,
    "CCT_2_TOTAL_PWR"        : 0x6A,
    "CCT_2_PHASE_A_PF"       : 0x7C,
    "CCT_2_PHASE_B_PF"       : 0x7E,
    "CCT_2_PHASE_C_PF"       : 0x80,
    "CCT_2_PHASE_A_KWH_OUT"  : 0x84,
    "CCT_2_PHASE_B_KWH_OUT"  : 0x86,
    "CCT_2_PHASE_C_KWH_OUT"  : 0x88,
    "CCT_2_PHASE_A_KWH_IN"   : 0x8C,
    "CCT_2_PHASE_B_KWH_IN"   : 0x8E,
    "CCT_2_PHASE_C_KWH_IN"   : 0x90,
    # ////////////////////////////////////
    "CCT_3_PHASE_A_CURRENT"  : 0xA4,
    "CCT_3_PHASE_B_CURRENT"  : 0xA6,
    "CCT_3_PHASE_C_CURRENT"  : 0xA8,
    "CCT_3_NEUTRAL_CURRENT"  : 0xAA,
    "CCT_3_PHASE_A_PWR"      : 0xAC,
    "CCT_3_PHASE_B_PWR"      : 0xAE,
    "CCT_3_PHASE_C_PWR"      : 0xB0,
    "CCT_3_TOTAL_PWR"        : 0xB2,
    "CCT_3_PHASE_A_PF"       : 0xC4,
    "CCT_3_PHASE_B_PF"       : 0xC6,
    "CCT_3_PHASE_C_PF"       : 0xC8,
    "CCT_3_PHASE_A_KWH_OUT"  : 0xCC,
    "CCT_3_PHASE_B_KWH_OUT"  : 0xCE,
    "CCT_3_PHASE_C_KWH_OUT"  : 0xD0,
    "CCT_3_PHASE_A_KWH_IN"   : 0xD4,
    "CCT_3_PHASE_B_KWH_IN"   : 0xD6,
    "CCT_3_PHASE_C_KWH_IN"   : 0xD8
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    fields_read =[
    "PHASE_A_VOLTAGE"        ,
    "PHASE_B_VOLTAGE"        ,
    "PHASE_C_VOLTAGE"        ,
    "LINE_A_B_VOLTAGE"       ,
    "LINE_B_C_VOLTAGE"       ,
    "LINE_C_A_VOLTAGE"       ,
    "FREQ_HZ"                ,
    # ////////////////////////////////////
    "CCT_1_PHASE_A_CURRENT"  ,
    "CCT_1_PHASE_B_CURRENT"  ,
    "CCT_1_PHASE_C_CURRENT"  ,
    "CCT_1_NEUTRAL_CURRENT"  ,
    "CCT_1_PHASE_A_PWR"      ,
    "CCT_1_PHASE_B_PWR"      ,
    "CCT_1_PHASE_C_PWR"      ,
    "CCT_1_TOTAL_PWR"        ,
    "CCT_1_PHASE_A_PF"       ,
    "CCT_1_PHASE_B_PF"       ,
    "CCT_1_PHASE_C_PF"       ,
    "CCT_1_PHASE_A_KWH_OUT"  ,
    "CCT_1_PHASE_B_KWH_OUT"  ,
    "CCT_1_PHASE_C_KWH_OUT"  ,
    "CCT_1_PHASE_A_KWH_IN"   ,
    "CCT_1_PHASE_B_KWH_IN"   ,
    "CCT_1_PHASE_C_KWH_IN"   ,
    # ////////////////////////////////////
    "CCT_2_PHASE_A_CURRENT"  ,
    "CCT_2_PHASE_B_CURRENT"  ,
    "CCT_2_PHASE_C_CURRENT"  ,
    "CCT_2_NEUTRAL_CURRENT"  ,
    "CCT_2_PHASE_A_PWR"      ,
    "CCT_2_PHASE_B_PWR"      ,
    "CCT_2_PHASE_C_PWR"      ,
    "CCT_2_TOTAL_PWR"        ,
    "CCT_2_PHASE_A_PF"       ,
    "CCT_2_PHASE_B_PF"       ,
    "CCT_2_PHASE_C_PF"       ,
    "CCT_2_PHASE_A_KWH_OUT"  ,
    "CCT_2_PHASE_B_KWH_OUT"  ,
    "CCT_2_PHASE_C_KWH_OUT"  ,
    "CCT_2_PHASE_A_KWH_IN"   ,
    "CCT_2_PHASE_B_KWH_IN"   ,
    "CCT_2_PHASE_C_KWH_IN"   ,
    # ////////////////////////////////////
    "CCT_3_PHASE_A_CURRENT"  ,
    "CCT_3_PHASE_B_CURRENT"  ,
    "CCT_3_PHASE_C_CURRENT"  ,
    "CCT_3_NEUTRAL_CURRENT"  ,
    "CCT_3_PHASE_A_PWR"      ,
    "CCT_3_PHASE_B_PWR"      ,
    "CCT_3_PHASE_C_PWR"      ,
    "CCT_3_TOTAL_PWR"        ,
    "CCT_3_PHASE_A_PF"       ,
    "CCT_3_PHASE_B_PF"       ,
    "CCT_3_PHASE_C_PF"       ,
    "CCT_3_PHASE_A_KWH_OUT"  ,
    "CCT_3_PHASE_B_KWH_OUT"  ,
    "CCT_3_PHASE_C_KWH_OUT"  ,
    "CCT_3_PHASE_A_KWH_IN"   ,
    "CCT_3_PHASE_B_KWH_IN"   ,
    "CCT_3_PHASE_C_KWH_IN"   
    ]
    
    def __init__(self, client: ModbusSerialClient, slave_id):
        self.client = client
        self.slave_id = slave_id 

    # def read_uint16(self, address: int) -> int:
    #     result = self.client.read_holding_registers(address, count=1, slave=self.slave_id)
    #     if result.isError():
    #         print(f"Error reading uint16 at address {address}")
    #         return None
    #     return result.registers[0]
    
    def read_float(self, address: int) -> float:
        try:
            result = self.client.read_holding_registers(address, count=2)
        except Exception as e:
            print(f"Exception reading float at address {address}: {e}")
            return float('nan')
        if result.isError():
            print(f"Error reading float at address {address}")
            return float('nan')
        # Combine two 16-bit registers into a 32-bit float
        high, low = result.registers
        byte_data = struct.pack('>HH', high, low)  # Big-endian
        return struct.unpack('>f', byte_data)[0]
    
    def get_all_data(self):
        for field in self.fields_read:
            addr = self.fields_to_addr[field]
            setattr(self, field.lower(), self.read_float(addr))
            # print(f"{field}: {getattr(self, field.lower())}")
            time.sleep(1 /1000 * 10)  # slight delay between reads

# --- Mapping the 9 Channels to the data fields for easy Python indexing ---
# This structure replaces the long C nested ternary operator.
# The order must exactly match the C code's conditional logic (ch=0 to ch=8)
CHANNEL_FIELDS = [
    # CCT 1
    ('cct_1_phase_a_current', 'cct_1_phase_a_pwr', 'cct_1_phase_a_pf', 'cct_1_phase_a_kwh_in', 'cct_1_phase_a_kwh_out'), # ch=0
    ('cct_1_phase_b_current', 'cct_1_phase_b_pwr', 'cct_1_phase_b_pf', 'cct_1_phase_b_kwh_in', 'cct_1_phase_b_kwh_out'), # ch=1
    ('cct_1_phase_c_current', 'cct_1_phase_c_pwr', 'cct_1_phase_c_pf', 'cct_1_phase_c_kwh_in', 'cct_1_phase_c_kwh_out'), # ch=2
    # CCT 2
    ('cct_2_phase_a_current', 'cct_2_phase_a_pwr', 'cct_2_phase_a_pf', 'cct_2_phase_a_kwh_in', 'cct_2_phase_a_kwh_out'), # ch=3
    ('cct_2_phase_b_current', 'cct_2_phase_b_pwr', 'cct_2_phase_b_pf', 'cct_2_phase_b_kwh_in', 'cct_2_phase_b_kwh_out'), # ch=4
    ('cct_2_phase_c_current', 'cct_2_phase_c_pwr', 'cct_2_phase_c_pf', 'cct_2_phase_c_kwh_in', 'cct_2_phase_c_kwh_out'), # ch=5
    # CCT 3
    ('cct_3_phase_a_current', 'cct_3_phase_a_pwr', 'cct_3_phase_a_pf', 'cct_3_phase_a_kwh_in', 'cct_3_phase_a_kwh_out'), # ch=6
    ('cct_3_phase_b_current', 'cct_3_phase_b_pwr', 'cct_3_phase_b_pf', 'cct_3_phase_b_kwh_in', 'cct_3_phase_b_kwh_out'), # ch=7
    ('cct_3_phase_c_current', 'cct_3_phase_c_pwr', 'cct_3_phase_c_pf', 'cct_3_phase_c_kwh_in', 'cct_3_phase_c_kwh_out'), # ch=8
]


class Telemetry:
    def __init__(self, timestamp, deviceID, msgID, lat, lng, rssi):
        self.timestamp = timestamp
        self.deviceID = deviceID
        self.msgID = msgID
        self.lat = lat
        self.lng = lng
        self.rssi = rssi
        
def parse_data(meters: List[PD194z], data: Telemetry) -> str:
    data_str = ''
    data_str +=  (
    f'{{"Timestamp":"{data.timestamp}","DeviceID":"{data.deviceID}","MsgID":"0x{data.msgID:04x}","Lat":"{data.lat:.6f}","Lng":"{data.lng:.6f}","RSSI":"{data.rssi}","meters":['
)
    for i, meter in enumerate(meters):
        data_str += f'{{"meter_type":"AC","ID":"meter{i +1}","phA_V":"{getattr(meter,"phase_a_voltage"):.1f}","phB_V":"{getattr(meter,"phase_b_voltage"):.1f}","phC_V":"{getattr(meter,"phase_c_voltage"):.1f}","freq":"{getattr(meter,"freq_hz"):.2f}","channels":['
        for ch in range(9):
            # 1. Look up the field names using the channel index
            current_field, pwr_field, pf_field, energy_in_field, energy_out_field = CHANNEL_FIELDS[ch]

            # 2. Get the actual values using getattr (safer than direct attribute access if used with dicts)
            # Note: If meter_data is a dictionary, use meter_data.get(field)
            current_val = getattr(meter, current_field)
            pwr_val = getattr(meter, pwr_field)
            pf_val = getattr(meter, pf_field)
            energy_in_val = getattr(meter, energy_in_field)
            energy_out_val = getattr(meter, energy_out_field)
            
            # 3. Replicate the conditional comma
            comma_or_none = "," if ch < 8 else ""

            # 4. Replicate the snprintf formatting using an f-string
            # The C code is appended to dataStr + offset. In Python, we append to a list.
            data_str += (
                f'{{"ID":"ch{ch + 1}","I":"{current_val:.3f}","P":"{pwr_val:.3f}",'
                f'"pF":"{pf_val:.3f}","KWh_In":"{energy_in_val:.3f}","KWh_Out":"{energy_out_val:.3f}"}}{comma_or_none}'
            )
        data_str += f']}}{"," if (i < len(meters) - 1) else ""}'
    data_str += f']}}'
    return data_str
    
current_working_directory = os.getcwd()
script_path = os.path.abspath(__file__)
print(f"Current working directory: {script_path}")
client = ModbusSerialClient(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )
if client.connect():
    print("Connected to Modbus RTU device")
else:
    print("Failed to connect to Modbus RTU device")
    exit(1)

meters = [PD194z(client, slave_id=i) for i in range(3)]  # Example with one meter
i = 0
tel = Telemetry(datetime.now(), "Device001", 0x00, 12.345678, 98.765432, -70)
while True:
    tel.msgID += 1
    i += 1
    tel.timestamp = datetime.now()
    for meter in meters:
        meter.get_all_data()
    with open(f"{current_working_directory}/meter_data/mData{i}.txt", "w") as f:
        f.write(parse_data(meters,tel ))
    time.sleep(40)
   