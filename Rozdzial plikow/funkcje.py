from szkielet import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import time
import grzalka
import miernik20
import csv

class program():
    def __init__(self):
        self.UI=Ui_MainWindow()
        self.okno = QtWidgets.QMainWindow()
        self.UI.setupUi(self.okno)

        self.kanaly=[0,0,0]

        self.pilk_wyjsciowy="test.cvs"
        
        self.p1=0
        self.p2=0

        self.moc=0
        self.czestotliwosc=4

        self.data_pomiaru = time.strftime("%d_%m_%Y_", time.localtime())
        self.plik_wyjsciowy="test"
        
        self.dane_raw=np.zeros([4,2])
        self.dane_przetworzone=np.zeros([2,3])

        self.arduino=grzalka.Grzanie()
        self.miernik=miernik20.Aparature()
        self.miernik.ustaw_r

        self.pomiar_start=0
        self.czas_0=0
        
        self.UI.label_przedrostek.setText(self.data_pomiaru)

        self.UI.comboBox_kanaly0.activated['int'].connect(self.zmiana_kanal0)
        self.UI.comboBox_kanaly1.activated['int'].connect(self.zmiana_kanal1)
        self.UI.comboBox_kanaly2.activated['int'].connect(self.zmiana_kanal2)
        
        self.UI.doubleSpinBox_czestotliowsc.valueChanged['double'].connect(self.zmiana_czestotliwosc)

        self.UI.nazwa_pliku.textChanged['QString'].connect(self.zmiana_nazwa)

        self.UI.horizontalSlider.valueChanged['int'].connect(self.zmiana_moc)
        self.UI.horizontalSlider.sliderReleased.connect(self.moc_do_arduino)

        self.UI.comboBox.activated['int'].connect(self.UI.stackedWidget.setCurrentIndex)

        self.UI.pushButton_start.clicked.connect(self.start_stop)


    def start_stop(self):
        self.UI.comboBox.setEnabled(False)
        self.UI.nazwa_pliku.setEnabled(False)
        
        if( self.pomiar_start == 0):
            self.pomiar_start=1
            self.UI.pushButton_start.setText("Stop")
            self.pomiar()
            if(self.czas_0==0):
                self.czas_0=time.time()
        else:
            self.pomiar_start=0
            self.UI.pushButton_start.setText("Start")
            self.timer_out.stop()
    
    def rysuj(self):
        self.przetworz()
        self.UI.wykres_1.dane=np.append(self.UI.wykres_1.dane,[[ self.dane_raw[3,0],self.dane_raw[3,1] ]],axis=0)
        self.UI.wykres_2.dane=np.append(self.UI.wykres_2.dane,[[self.dane_przetworzone[0,0],self.dane_przetworzone[0,1],self.dane_przetworzone[0,2] ]],axis=0)
        self.UI.wykres_3.dane=np.append(self.UI.wykres_3.dane,[self.dane_przetworzone[1]],axis=0)
        self.UI.wykres_1.update_figure()
        self.UI.wykres_2.update_figure()
        self.UI.wykres_3.update_figure()

    def przetworz(self):
        a=(self.dane_raw[0,1]-self.dane_raw[3,1])/(self.dane_raw[0,0]-self.dane_raw[3,0])
        b=self.dane_raw[0,1]-a*self.dane_raw[0,0]

        self.dane_przetworzone[0,0]=self.dane_raw[1,0]
        self.dane_przetworzone[0,1]=a*self.dane_raw[1,0]+b
        self.dane_przetworzone[0,2]=self.dane_raw[1,1]
        self.dane_przetworzone[1,0]=self.dane_raw[2,0]
        self.dane_przetworzone[1,1]=a*self.dane_raw[2,0]+b
        self.dane_przetworzone[1,2]=self.dane_raw[2,1]


    def zmiana_moc(self,w):
        self.moc=w
        self.UI.label_aktualna_moc_wartosc.setText(str(self.moc))

    def zmiana_czestotliwosc(self,f):
        self.czestotliwosc=f
    
    def zmiana_nazwa(self,n):
        self.plik_wyjsciowy=self.data_pomiaru+n
        self.UI.label_tytul2.setText(n)

    def moc_do_arduino(self):
        self.arduino.zmien_moc(self.moc)

    def zmiana_kanal0(self,ch):
        self.kanaly[0]=ch+1

    def zmiana_kanal1(self,ch):
        self.kanaly[1]=ch+1

    def zmiana_kanal2(self,ch):
        self.kanaly[2]=ch+1

    def zapis_prztworzone(self,t,T,p1,p2):
        with open(self.pilk_wyjsciowy,"a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow( [t, T, p1, p2])

    def pomiar(self):
        print("start")
        self.timer_out = QtCore.QTimer()
        self.pomiar_in_a()
        self.timer_out.timeout.connect(self.pomiar_in_a)
        self.timer_out.start(1000*self.czestotliwosc)

    def pomiar_in_a(self):
        print("#########")
        self.p1=0
        self.p2=0
        self.timer_in = QtCore.QTimer()
        self.pomiar_in_b()
        self.timer_in.timeout.connect(self.pomiar_in_b)
        self.timer_in.start(200)

    def pomiar_in_b(self):
        print("---")
        if(self.p1<4):
            if(self.p2==0):
                self.miernik.zamknij(self.kanaly[self.p1%3])
                print(time.time()-self.czas_0)
                self.p2=1
            else:
                self.dane_raw[self.p1,0]=time.time()-self.czas_0
                self.dane_raw[self.p1,1]=self.miernik.mierz()
                print( "odzczyt nr " +str(self.p1+1))                 
                print(self.dane_raw[self.p1,1])
                self.p1+=1
                self.p2=0
        else:
            self.rysuj()
            self.timer_in.stop()
