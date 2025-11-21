import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Define the data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 50),
    co=ModbusSequentialDataBlock(0, [0] * 100),
    hr=ModbusSequentialDataBlock(0, [0x32] * 100),
    ir=ModbusSequentialDataBlock(0, [0] * 100)
)
context = ModbusServerContext(slaves=store, single=True)

# Start the Modbus TCP server
StartTcpServer(context=context, address=("127.0.0.1", 1502))