#!/home/pai/Documents/sunspec_pai/bin/python
from pymodbus.client import ModbusSerialClient
from modbus_utils import *
import time
class Meter:
    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        self.client = modbus_client
        self.slave_id = slave_id
        
    def read_voltage_a(self) -> float:
        pass

    def read_frequency(self) -> float:
        pass
    
    def read_current_a(self) -> float:
        pass
    
    def read_power_a(self) -> float:
        pass
    
    def read_pf_a(self) -> float:
        pass
    
    def read_energy_a(self) -> float:
        pass
    
    
class ADL200N(Meter):
    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        Meter.__init__(self, modbus_client, slave_id)

    def read_voltage_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x2000, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_frequency(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x2134, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
        
    def read_current_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x200C, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_power_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x2014, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_pf_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x202C, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_energy_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x3020, count = 4,slave = self.slave_id)
            return hold_reg_to_float64(result.registers[0], result.registers[1], result.registers[2], result.registers[3])
        except Exception as e:
            return float('nan')

class ADW300N(Meter):
    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        Meter.__init__(self, modbus_client, slave_id)

    def read_voltage_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0014, count = 1,slave = self.slave_id)
            return result.registers[0] * 0.1
        except Exception as e:
            return float('nan')
        
    def read_frequency(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x003B, count = 1,slave = self.slave_id)
            return result.registers[0] * 0.01
        except Exception as e:
            return float('nan')
        
    def read_current_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x001A, count = 1,slave = self.slave_id)
            return result.registers[0] * 0.01 * 4
        except Exception as e:
            return float('nan')
        
    def read_power_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x001E, count = 2,slave = self.slave_id)
            return hold_reg_to_uint32(result.registers[0], result.registers[1]) * 0.001 * 4
        except Exception as e:
            return float('nan')
        
    def read_pf_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0036, count = 1,slave = self.slave_id)
            return result.registers[0] * 0.001
        except Exception as e:
            return float('nan')
        
    def read_energy_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x004A, count = 2,slave = self.slave_id)
            return hold_reg_to_uint32(result.registers[0], result.registers[1]) * 0.01
        except Exception as e:
            return float('nan')
        
class ADL400N:
    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        self.client = modbus_client
        self.slave_id = slave_id

    def read_voltage_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0061, count = 1,slave = self.slave_id)
            return result.registers[0] * 0.1
        except Exception as e:
            return float('nan')
    
    def read_frequency(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0077, count = 1,slave = self.slave_id)
            return hold_reg_to_uint16(result.registers[0])* 0.01
        except Exception as e:
            return float('nan')
        
    def read_current_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0064, count = 1,slave = self.slave_id)
            return hold_reg_to_uint16(result.registers[0])* 0.01 * 60
        except Exception as e:
            return float('nan')
        
    def read_power_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0164, count = 2,slave = self.slave_id)
            return hold_reg_to_uint32(result.registers[0], result.registers[1]) * 0.001 * 60
        except Exception as e:
            return float('nan')
        
    def read_pf_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x017C, count = 1,slave = self.slave_id)
            return result.registers[0] * 0.001
        except Exception as e:
            return float('nan')
        
    def read_energy_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0087, count = 2,slave = self.slave_id)
            return hold_reg_to_uint32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
class PD194Z(Meter):
    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        Meter.__init__(self, modbus_client, slave_id)
    
    def read_voltage_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x000A, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_frequency(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0012, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_current_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0018, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_power_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0020, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
    def read_pf_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0038, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_energy_a(self) -> float:
        try:
            result = self.client.read_holding_registers(address = 0x0040, count = 4,slave = self.slave_id)
            return hold_reg_to_float64(result.registers[0], result.registers[1], result.registers[2], result.registers[3])
        except Exception as e:
            return float('nan')
        
class SDM630MCT(Meter):
    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        Meter.__init__(self, modbus_client, slave_id)
    
    def read_voltage_a(self) -> float:
        try:
            result = self.client.read_input_registers(address = 0x0000, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_frequency(self) -> float:
        try:
            result = self.client.read_input_registers(address = 0x0046, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_current_a(self) -> float:
        try:
            result = self.client.read_input_registers(address = 0x0006, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_power_a(self) -> float:
        try:
            result = self.client.read_input_registers(address = 0x000C, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1]) / 1000
        except Exception as e:
            return float('nan')
        
    def read_pf_a(self) -> float:
        try:
            result = self.client.read_input_registers(address = 0x001E, count = 2,slave = self.slave_id)
            return hold_reg_to_float32(result.registers[0], result.registers[1])
        except Exception as e:
            return float('nan')
        
    def read_energy_a(self) -> float:
        try:
            result = self.client.read_input_registers(address = 0x004A, count = 4,slave = self.slave_id)
            return hold_reg_to_float64(result.registers[0], result.registers[1], result.registers[2], result.registers[3])
        except Exception as e:
            return float('nan')