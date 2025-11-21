from pymodbus.client import ModbusSerialClient
from modbus_utils import *
import struct
import time
class SunSpecSystem:
    # SunSpec marker (ASCII "SunS" → 0x53756E53)
    SUNS_MARKER = 0x53756E53
    REGISTER_LOCATIONS = [40000, 0, 50000]
    def __init__(self,  client: ModbusSerialClient, slave_id):
        self.client = client
        self.models = []
        self.slave_id = slave_id 

    def read_float_field(self, base_addr, offset_attr, target_attr):
        addr = base_addr + getattr(self, offset_attr) - 1
        setattr(self, target_attr, read_float(client = self.client, address = addr, slave = self.slave_id))

    def read_uint16_field(self, base_addr, offset_attr, target_attr):
        addr = base_addr + getattr(self, offset_attr) - 1
        setattr(self, target_attr, read_uint16(client= self.client, address = addr, slave = self.slave_id))
            
    def read_sunspec_models(self):
        self.sunspec_base_addr = self.get_sunspec_addr(self.slave_id)
        # Step 2: Read SunSpec models
        addr = self.sunspec_base_addr + 2  # skip the marker (2 registers)
        if not (self.client.is_socket_open or self.client.connect()):
            return None

        while True:
            result = self.client.read_holding_registers(addr, count = 2, device_id =self.slave_id)
            if result.isError():
                print(f"Error reading at address {addr}")
                break

            model_id = result.registers[0]
            length = result.registers[1]

            if model_id == 0xFFFF:
                print("End of model list.")
                break

            print(f"Model ID: {model_id} at address {addr}, length: {length}")
            self.models.append((addr, model_id, length))

            addr += 2 + length  # 2 for ID + length, then skip model data

            time.sleep(0.05)  # add slight delay between reads if needed

        self.client.close()
             


        return False
    
    def get_sunspec_addr(self, slave):
        # Open connection
        if not (self.client.is_socket_open or self.client.connect()):
            print("Failed to connect to Modbus RTU device")
            return None
        # Step 1: Search for SunSpec marker
        
        for addr in SunSpecSystem.REGISTER_LOCATIONS:
            val = read_uint32(client=self.client, address= addr, slave = self.slave_id)
            print(f"Value at address {addr} is {val}")
            if val == SunSpecSystem.SUNS_MARKER:
                print(f"SunSpec marker found at address {addr}")
                return addr

    


class FruniouEcoPara(SunSpecSystem):

    INVERTER_MODEL_ID = 113

    ID = 1
    L =2
    A = 3
    AphA = 5
    AphB = 7
    AphC = 9
    PPVphAB = 11
    PPVphBC = 13
    PPVphCA = 15
    PhVphA= 17
    PhVphB= 19
    PhVphC = 21
    W = 23
    Hz = 25
    VA = 27
    VAr = 29
    PF = 31
    WH = 33
    DCA = 35
    DCV = 37
    DCW = 39 
    TmpCab = 41
    TmpSnk = 43
    TmpTrns = 45
    TmpOt = 47
    St = 49

    def __init__(self, slave_id):
        client = ModbusSerialClient(
            port='/dev/ttyUSB1',
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )
        super().__init__(client, slave_id)
        self.ac_current = 0

        self.ph_a_current = 0
        self.ph_b_current = 0
        self.ph_c_current = 0
    
        self.ph_ab_voltage = 0
        self.ph_bc_voltage = 0
        self.ph_ca_voltage = 0
    
        self.ph_an_voltage = 0
        self.ph_bn_voltage = 0
        self.ph_cn_voltage = 0
    
        self.ac_pwr = 0
        self.ac_freq = 0

        self.ac_va = 0
        self.ac_var = 0
        self.ac_pf = 0
        self.ac_energy = 0
        self.dc_current = 0
        self.dc_voltage = 0
        self.dc_power = 0
        self.tmp_cab = 0
        self.tmp_trns = 0
        self.tmp_ot = 0
        self.state = 0

        self.fields_to_read = [
            ('A', 'ac_current'),
            ('AphA', 'ph_a_current'),
            ('AphB', 'ph_b_current'),
            ('AphC', 'ph_c_current'),
            ('PPVphAB', 'ph_ab_voltage'),
            ('PPVphBC', 'ph_bc_voltage'),
            ('PPVphCA', 'ph_ca_voltage'),
            ('PhVphA', 'ph_an_voltage'),
            ('PhVphB', 'ph_bn_voltage'),
            ('PhVphC', 'ph_cn_voltage'),
            ('W', 'ac_pwr'),
            ('Hz', 'ac_freq'),
            ('VA', 'ac_va'),
            ('VAr', 'ac_var'),
            ('PF', 'ac_pf'),
            ('WH', 'ac_energy'),
            ('DCA', 'dc_current'),
            ('DCV', 'dc_voltage'),
            ('DCW', 'dc_power'),
            ('TmpCab', 'tmp_cab'),
        ]
    
   

    def read_inverter_parameter(self) -> bool:
        if len(self.models) == 0:
            self.read_sunspec_models()
            if len(self.models) == 0:
                return False

        for model in self.models:
            if model[1] == self.INVERTER_MODEL_ID:
                base_addr = model[0]
                for offset_attr, target_attr in self.fields_to_read:
                    self.read_float_field(base_addr, offset_attr, target_attr)
                self.read_uint16_field(base_addr, 'St', 'state')
                break

        return True
    

    def test_system(self):
        self.read_sunspec_models()
        self.read_inverter_parameter()
        for _, attr in self.fields_to_read:
            print(attr, getattr(self, attr))
        print('state', getattr(self,'state'))


frunious = FruniouEcoPara(1)
frunious.test_system()



