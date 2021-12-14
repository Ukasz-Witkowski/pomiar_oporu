import serial
import find_com

class Grzanie:

    def __init__(self):
        com = find_com.find_device('CH340')   #klon arduino
        #com = find_com.find_device('Arduino')   #Arduino Leonarado
        self.arduino = serial.Serial(com, baudrate=9600, timeout=1)


    def zmien_moc(self, moc):
        data_to_arduino = str(moc)+'\n'
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))

