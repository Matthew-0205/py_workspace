from pymodbus.client import ModbusTcpClient
from time import sleep
client = ModbusTcpClient("127.0.0.1", port=1502)

for i in range(100000):
    client.connect()
    result = client.read_holding_registers(0, count =7)
    print(result.registers if result.isError() is False else result)
    client.close()

# import socket
# import struct

# host = '127.0.0.1'
# port = 1502

# transaction_id = 1
# protocol_id = 0
# unit_id = 1
# function_code = 3  # Read Holding Registers
# start_address = 0
# quantity = 2

# request_pdu = struct.pack('>BHH', function_code, start_address, quantity)
# length = len(request_pdu) + 1
# mbap_header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
# message = mbap_header + request_pdu
# print(",essage:", message)
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#     client_socket.connect((host, port))
#     client_socket.sendall(message)
#     data = client_socket.recv(1024)
#     print("Received:", data)
# finally:
#     client_socket.close()
