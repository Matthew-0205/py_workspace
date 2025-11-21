


#!/home/pai/Documents/sunspec_pai/bin/python
from datetime import datetime
import os
from pymodbus.client import ModbusSerialClient
from modbus_utils import *
import time

current_working_directory = os.getcwd()
script_path = os.path.abspath(__file__)

class SolarIrradiationSensor:
    def __init__(self,slave_id: int, client: ModbusSerialClient):
        self.client: ModbusSerialClient = client
        self.slave_id: int = slave_id
    
    def read_irradiation(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0000, count = 1,slave = self.slave_id)
        except Exception as e:
            print(f"Exception reading level from ultrasonic sensor at address {self.slave_id}: {e}")
            return float('nan')
        if not result.isError():
            return hold_reg_to_uint16(result.registers[0])
        else:
            print(f"Error reading level from ultrasonic sensor at address {self.slave_id} ")
            return float('nan')
        
    def set_slave_id(self, new_slave_id: int) -> bool:
        result = self.client.write_register(address=0x07D0, value=new_slave_id, slave=self.slave_id)
        if not result.isError():
            self.slave_id = new_slave_id
            print(f"Slave ID changed to {new_slave_id}")
            self.slave_id = new_slave_id
            return True
        else:
            print(f"Error changing slave ID to {new_slave_id}")
            return False

# Configure client
client = ModbusSerialClient(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

# Connect to the device
if client.connect():
    print("Connected to Modbus device")
else:
    print("Failed to connect to Modbus device")
    exit()

sensor = SolarIrradiationSensor(slave_id=1,  client=client)

with open(f"{current_working_directory}/solar_irradiation_readings_{datetime.now()}.csv", "w") as file:
    file.write("S_N,Timestamp,Irradiation_W_m2\n")
    s_n = 0
    while 1:
        irradiation = sensor.read_irradiation()
        file.write(f"{s_n},{irradiation},{datetime.now()}\n")
        # print(f"{s_n},{irradiation},{datetime.now()}")
        time.sleep(1)
        s_n += 1

client.close()
