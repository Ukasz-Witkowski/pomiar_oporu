#ten program komunikuje się z miernikiem i ryzuje wykres opory w zależności od czasu ale tylko z głównego kanału, dodatkowo zapisuje dane w excelu

import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pyvisa

class Aparature:
    adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.miernik = rm.open_resource(self.adres_miernika)

    def measurement(self):
        pomiar = self.miernik.query("MEAS:RES?")
        return pomiar

nasz_miernik = Aparature()

plot_window = 20
y_var = np.array(np.zeros([plot_window]))

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(y_var)

while True:
    
    data = float(nasz_miernik.measurement())
    print(data)
    with open("test_data.csv","a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([time.time(), data])
    y_var = np.append(y_var, data )
    y_var = y_var[1 : plot_window + 1]
    line.set_ydata(y_var)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.5)
