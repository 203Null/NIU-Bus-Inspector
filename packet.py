from termcolor import colored
import matplotlib.pyplot as plt
import numpy as np

class niuPacket:
    unit = ""
    color = "white"
    data = []

    def __init__(self):
        pass

    def __init__(self, unit, color):
        self.unit = unit
        self.color = color

    def pushByte(self, byte):
        byte = int.from_bytes(byte, "big")

        if len(self.data) == 0 and byte != 0x68:
            # print(colored(f"Skipped {byte:02x} ", self.color))
            return False

        if len(self.data) == 3 and byte != 0x68:
            # print(colored(f"Skipped {byte:02x} ", self.color))
            self.data = []
            return False

        self.data.append(byte)
        if len(self.data) >= 8 and len(self.data) >= self.data[5] + 8:
            self.parseData()
            self.data = []
            return True

        if len(self.data) > 255:
            print(colored("error, oversized package", self.color))
            for b in self.data:
                print(colored(f"{b:02x} ", self.color), end="")
            print()
            self.data = []
        return False

    def parseData(self):
        unknown = self.data[1]
        device = self.data[2]
        # response = self.data[4] >= 0x80
        # control_type = self.data[4] % 0x10
        control_type = self.data[4]
        length = self.data[5]
        # message_type = self.data[6]

        checksum = self.getCheckSum(self.data[:self.data[5] + 6])
        vaild = self.data[0] == 0x68 and self.data[self.data[5] + 7] == 0x16 and self.data[self.data[5] + 6] == checksum

        data = []
        for i in range(6, 6 + length):
            data.append((self.data[i] - 0x33) % 0x100)

        if vaild == False:
            return

        # if response == False:
        if device == 0xde:
            if control_type == 0x04:
                if data[0] == 0x06:
                    unknown_val = data[1]
                    throttle = (data[2] * 255) + self.data[4]
                    r_brake = (data[4] * 255) + self.data[5]
                    f_brake = (data[6] * 255) + self.data[7]
                    print(colored(f"Vehicle Control - Throttle: {throttle} R Break: {r_brake} F Break: {f_brake}", self.color))
                    return
            #     # elif data[0] == 0x19:
            #     #     pass
            #     # elif data[0] == 0x0F:
            #     #     pass
            #     # elif data[0] == 0x01:
            #     #     pass
            # # elif control_type == 0x01: #Read
            # #     return
            # elif control_type == 0x03: #Write
            #     value = data[1] * 255 + data[2]
            #     print(colored(f"Set reg {hex(data[0])} to {hex(value)}", self.color))
            #     # return
            # elif control_type == 0x81:
            #     print(colored(f"Reg read (0x81) result: ", self.color))
            #     for val in data:
            #         print(colored(f"{val :02x} ", self.color), end="")
            #     print()
            #     # return
            # elif control_type == 0x82:
            #     print(colored(f"Reg read (0x82) result: ", self.color))
            #     for val in data:
            #         print(colored(f"{val :02x} ", self.color), end="")
            #     print()
            #     # return
            # elif control_type == 0x83:
            #     print(colored(f"Reg wrote", self.color))
            #     # return
            if control_type == 0x84:
                # 02   00 00 00 30 00 00 43 00 01  00 00 00 00 eb 16 00 00 00 01 00 00 00 00
                # Mode             Speed    changes changes
                mode = data[0]
                val1 = (data[1] * 255) + data[2]
                val2 = (data[3] * 255) + data[4]
                speed = (data[5] * 255) + data[6]
                val4 = (data[8] * 255) + data[9] #Works like gear in ICE car
                val5 = (data[10] * 255) + data[11] #Whell
                # val6 = (data[11] * 255) + data[12]
                # val7 = (data[13] * 255) + data[14]
                # val8 = (data[15] * 255) + data[16]
                # val9 = (data[17] * 255) + data[18]
                print(colored(f"Vehicle Status - Mode: {mode} Speed: {speed/10} KM/h {[val4, val5]}", self.color))
                return
            # else:
            #     return
        # else:
        #     return

        # elif device == 0xce: #Battery
        #     if control_type == 0x82:
        #         battery_percentage = data[6]
        #         print(colored(f"Battery Status - Percentage: {battery_percentage}%", self.color))
        #         return

        #Unknown Data
        print(colored(f"{self.unit} - ", self.color), end="")
        print(colored("Raw: ", self.color), end="")
        for b in self.data:
            print(colored(f"{b:02x} ", self.color), end="")
        print()

        print(colored(f"{self.unit} - ", self.color), end="")
        print(colored("Header: ", self.color), end="")
        for i in range(1, 5):
            print(colored(f"{self.data[i]:02x} ", self.color), end="")

        print(colored(f"Len: {length:02x} ", self.color), end="")

        print(colored(f"Data: ", self.color), end="")
        for val in data:
            print(colored(f"{val :02x} ", self.color), end="")
        print()


    def addOffset(self, num): #Only for < 0xFF
        return (num + 0x100 + 0x33) % 0x100

    def getCheckSum(self, list):
        checksum = 0
        for i in list:
            checksum += i
        checksum %= 0x100
        return checksum
