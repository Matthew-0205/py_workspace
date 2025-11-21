#!/home/pai/Documents/sunspec_pai/bin/python
from pymodbus.client import ModbusSerialClient
from modbus_utils import *



    

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
count = 313
modbus_max_count = 125
addr = 40000
c_list = '#include <stdint.h>\nconst uint16_t  buffer[] = {'
while count > 0:
    tmp_count = count
    if (tmp_count > 125):
        tmp_count = 125

    result = client.read_holding_registers(address = addr , count = tmp_count,slave = 1)
    if not result.isError():
        count -= tmp_count
        addr += tmp_count
        
        for reg in result.registers:
            # tmp_list= struct.unpack('>BB',struct.pack('>H', reg))
            # for temp in tmp_list:
            c_list += f"{hex(reg)}, "
    
c_list+= '};\n'
f = open ("c_list_file.h", 'a')
f.write(c_list)
f.close()

            

# Close connection
client.close()
