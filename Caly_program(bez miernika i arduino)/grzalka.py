# import serial
# import time
# import find_com
# import math

class Grzanie:

    def __init__(self):
        print("Polaczono z arduino")
        # com = find_com.find_device('CH340')
        # self.arduino = serial.Serial(com, baudrate=9600, timeout=1)


    def zmien_moc(self, moc):
        print("Zmieniono moc")
        # data_to_arduino = str(moc)+'\n'
        # self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))

