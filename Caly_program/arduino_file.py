import serial
import time
import pyvisa
import find_com
import math

class Aparature:

    def __init__(self):
    #    try:
        com = find_com.find_device('CH340')
        self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
  #      except OSError:
 #           errors.append('Płytka Arduino')

    def change_position(self, moc):
        data_to_arduino = str(moc)+'\n'
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))
        # while True:
        #     distance_made = self.arduino.readline().decode()
        #     if len(distance_made) > 0:
        #         return int(distance_made)

ar=Aparature()

time.sleep(2)
ar.change_position(20)
time.sleep(2)
ar.change_position(30)
time.sleep(2)
ar.change_position(40)