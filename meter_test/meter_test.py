#!/home/pai/Documents/sunspec_pai/bin/python
from meters import *
     
from datetime import datetime
import os
 
current_working_directory = os.getcwd()
script_directory = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.abspath(__file__)

   
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


meters: dict[str, Meter] = {
        'PD194Z': PD194Z(modbus_client=client, slave_id=2),
        'ADW300N': ADW300N(modbus_client=client, slave_id=82),
        'ADL200N': ADL200N(modbus_client=client, slave_id=1),
        'ADL400N': ADL400N(modbus_client=client, slave_id=81),
        'SDM630MCT': SDM630MCT(modbus_client=client, slave_id=61)}
s_n = 0
start_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

voltage_file_name = f"{script_directory}/meters_voltages_reading_{start_date}.csv"
voltage_file = open(voltage_file_name, "w")
voltage_file.write("s_n, PDI194Z, ADW300N, ADL200N, ADL400N, SDM630MCT\n")
voltage_file.close()


current_file_name = f"{script_directory}/meters_currents_reading_{start_date}.csv"
current_file = open(current_file_name, "w")
current_file.write("s_n, PDI194Z, ADW300N, ADL200N, ADL400N, SDM630MCT\n")
current_file.close()


power_file_name = f"{script_directory}/meters_powers_reading_{start_date}.csv"
power_file = open(power_file_name, "w")
power_file.write("s_n, PDI194Z, ADW300N, ADL200N, ADL400N, SDM630MCT\n")
power_file.close()

pf_file_name = f"{script_directory}/meters_pfs_reading_{start_date}.csv"
pf_file = open(pf_file_name, "w")
pf_file.write("s_n, PDI194Z, ADW300N, ADL200N, ADL400N, SDM630MCT\n")
pf_file.close()

frequency_file_name = f"{script_directory}/meters_frequencies_reading_{start_date}.csv"
frequency_file = open(frequency_file_name, "w")
frequency_file.write("s_n, PDI194Z, ADW300N, ADL200N, ADL400N, SDM630MCT\n")
frequency_file.close()

while True:
    voltage_a_s = f'{s_n},{datetime.now()},{datetime.now()},'
    for meter_name, meter in meters.items():
        voltage_a_s += f'{meter.read_voltage_a()},'
    voltage_a_s = voltage_a_s.rstrip(',')
    
    voltage_file = open(voltage_file_name, "a")
    voltage_file.write(f"{voltage_a_s}\n")
    voltage_file.close()
    
    current_a_s = f'{s_n},{datetime.now()},'
    for meter_name, meter in meters.items():
        current_a_s += f'{meter.read_current_a()},'
    current_a_s = current_a_s.rstrip(',')
    
    current_file = open(current_file_name, "a")
    current_file.write(f"{current_a_s}\n")
    current_file.close()
    
    
    power_a_s = f'{s_n},{datetime.now()},'
    for meter_name, meter in meters.items():
        power_a_s += f'{meter.read_power_a()},'
    power_a_s = power_a_s.rstrip(',')
    
    power_file = open(power_file_name, "a")
    power_file.write(f"{power_a_s}\n")
    power_file.close()
    
    pf_a_s = f'{s_n},{datetime.now()},'
    for meter_name, meter in meters.items():
        pf_a_s += f'{meter.read_pf_a()},'
    pf_a_s = pf_a_s.rstrip(',')
    
    pf_file = open(pf_file_name, "a")
    pf_file.write(f"{pf_a_s}\n")
    pf_file.close()


    frequency_a_s = f'{s_n},{datetime.now()},'
    for meter_name, meter in meters.items():
        frequency_a_s += f'{meter.read_frequency()},'
    frequency_a_s = frequency_a_s.rstrip(',')
    
    frequency_file = open(frequency_file_name, "a")
    frequency_file.write(f"{frequency_a_s}\n")
    frequency_file.close()
    
    
    s_n += 1
    time.sleep(30)
    
    
    
print(f"Voltage A readings: {voltage_a_s}")

# pd194z = PD194Z(modbus_client=client, slave_id=2) 
# voltage_a = pd194z.read_power_a()
# print(f"Voltage A: {voltage_a}")

# adw300_sensor = ADW300N(modbus_client=client, slave_id=82)
# voltage_a = adw300_sensor.read_current_a()
# print(f"Voltage A: {voltage_a}")

# adl200n_sensor = ADL200N(modbus_client=client, slave_id=1)
# voltage_a = adl200n_sensor.read_current_a()
# print(f"Voltage A: {voltage_a}")

# adl400n_sensor = ADL400N(modbus_client=client, slave_id=81)
# voltage_a = adl400n_sensor.read_voltage_a()
# print(f"Voltage A: {voltage_a}")

# sdm630mct = SDM630MCT(modbus_client=client, slave_id=61) 
# voltage_a = sdm630mct.read_power_a()
# print(f"Voltage A: {voltage_a}")