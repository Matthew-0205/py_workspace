from pymodbus.client import ModbusSerialClient
import struct

def hold_reg_to_float32(register0, register1) -> float:
    return struct.unpack(">f", struct.pack('>HH', register0, register1))[0]

def hold_reg_to_uint16(register) -> float:
    return struct.unpack(">H", struct.pack('>H', register))[0]

def hold_reg_to_uint32(register0, register1) -> float:
    return struct.unpack(">I", struct.pack('>HH', register0, register1))[0]

def hold_reg_to_int16(register) -> float:
    return struct.unpack(">h", register)[0]

def hold_reg_to_int32(register0, register1) -> float:
    return struct.unpack(">i", struct.pack('>HH', register0, register1))[0]

def hold_reg_to_string(raw_register, num_reg) -> str:
    return struct.unpack(f">{num_reg}h", raw_register)[0]



def read_float(client: ModbusSerialClient, address, slave ):
    result = client.read_holding_registers(address = address, count = 2,device_id = slave)
    if not result.isError():
        return hold_reg_to_float32(result.registers[0], result.registers[1])
    else: 
        print(f"Error reading float at address {address}")

def read_int16(client: ModbusSerialClient, address, slave ):
    result = client.read_holding_registers(address = address, count = 2,device_id = slave)
    if not result.isError():
        return hold_reg_to_int16(result.registers[0])
    else: 
        print(f"Error reading int16 at address {address}")
    
def read_uint16(client: ModbusSerialClient, address, slave):
    result = client.read_holding_registers(address = address, count = 2,device_id = slave)
    if not result.isError():
        return hold_reg_to_uint16(result.registers[0])
    else: 
        print(f"Error reading uint16 at address {address}")
      
def read_int32(client: ModbusSerialClient, address, slave):
    result = client.read_holding_registers(address = address, count = 2,device_id = slave)
    if not result.isError():
        return hold_reg_to_int32(result.registers[0], result.registers[1])
    else: 
        print(f"Error reading int32 at address {address}")
    
def read_uint32(client: ModbusSerialClient, address, slave):
    result = client.read_holding_registers(address = address, count = 2,device_id= slave)
    if not result.isError():
        return hold_reg_to_uint32(result.registers[0], result.registers[1])
    else: 
        print(f"Error reading uint32 at address {address}")
    
def read_string(client: ModbusSerialClient, address, len, slave):
    result = client.read_holding_registers(address = address, count = len,device_id = slave)
    if not result.isError():
        return hold_reg_to_uint32(result.registers[0], result.registers[1])
    else: 
        print(f"Error reading string at address {address}")