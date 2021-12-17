import serial
import find_com

class Grzanie:

    def __init__(self):
        self.error=0
        try:
            com = find_com.find_device('CH340') 
            self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
        except:
            print("nie ma grzałki")
            self.error=1
            
    def zmien_moc(self, moc):
        data_to_arduino = str(moc)+'\n'
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))

