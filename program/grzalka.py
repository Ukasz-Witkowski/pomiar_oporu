import serial

import serial.tools.list_ports

class Grzanie:

    def __init__(self):
        self.error=0
        try:
            com = find_device('CH340') 
            self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
        except:
            print("nie ma grzałki")
            self.error=1
            
    def zmien_moc(self, moc):
        data_to_arduino = str(moc)+'\n'
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))


def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


def find_device(name):
    comcomm_port = 'None'
    ports_found = get_ports()
    for port in ports_found:
        str_port = str(port)
        if name in str_port:
            split_port = str_port.split(' ')
            comcomm_port = (split_port[0])
    return comcomm_port
            

# if __name__ == '__main__':
#     connect_port = find_device('CH340')  # 'CH340'-Arduino clone name
#     all_ports = get_ports()
#     for port in all_ports:
#         x = str(port)
#         print(x)
#         x = x.split(' ')
#         print('split\n', x)
