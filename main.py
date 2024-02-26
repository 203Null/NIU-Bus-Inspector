import serial
from packet import niuPacket
from termcolor import colored


# mcu = serial.Serial('COM40', 38400, parity=serial.PARITY_EVEN)
bsc = serial.Serial('COM39', 38400, parity=serial.PARITY_EVEN)

# mcu_packet = niuPacket("MCU", "cyan")
bsc_packet = niuPacket("BSC", "magenta")
while True:
    # while mcu.inWaiting() > 0:
    #     if mcu_packet.pushByte(mcu.read()):
    #         break
    while bsc.inWaiting() > 0:
        if(bsc_packet.pushByte(bsc.read())):
            break



