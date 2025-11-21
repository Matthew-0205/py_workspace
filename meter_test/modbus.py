#!/home/pai/Documents/sunspec_pai/bin/python
from pymodbus.client import ModbusSerialClient
from modbus_utils import *
import time


    

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
client.connect()
start_time = time.perf_counter()
result = client.read_holding_registers(address = 0x0060, count = 10, slave = 81)
# result = client.write_register(address=0x07D1, value=2, slave=1)
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Function execution time: {elapsed_time:.4f} seconds")

# voltage = read_uint32(client=client,address= 40000)

print(f"Voltage: { [(x) for x in result.registers]}") 

# Close connection
client.close()
