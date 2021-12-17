from szkielet import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import time
import grzalka
import miernik20
import csv
import wykres
import json
from okno_ustawienia import Ui_Dialog as Form1
from okno_pomoc import Ui_Dialog as Form2
from PyQt5.QtWidgets import QMessageBox

class program():
    def __init__(self):
        self.UI=Ui_MainWindow()
        self.okno = QtWidgets.QMainWindow()
        self.UI.setupUi(self.okno)

        self.wykres_0 = wykres.Wykres_temp(self.UI.widget_temp,width=450/90,height=270/90, dpi=90)
        self.wykres_1 = wykres.Wykres_probka(self.UI.widget_probka1,width=530/90,height=310/90, dpi=90)
        self.wykres_2 = wykres.Wykres_probka(self.UI.widget_probka2,width=530/90,height=310/90, dpi=90)

        self.reset()

        self.A=0.385
        self.B=5.15

        self.arduino=grzalka.Grzanie()


        if(self.arduino.error==1):
            self.UI.horizontalSlider.setEnabled(False)  
            self.timer_kom1 = QtCore.QTimer()
            self.timer_kom1.timeout.connect(self.komunikat_grzalka)
            self.timer_kom1.timeout.connect(self.timer_kom1.stop)
            self.timer_kom1.start(1000)

        self.miernik=miernik20.Aparature()
        if(self.miernik.error==1):
            self.UI.pushButton_start.setEnabled(False)
            self.UI.pushButton_start2.setEnabled(False)
   
            self.timer_kom2 = QtCore.QTimer()
            self.timer_kom2.timeout.connect(self.komunikat_miernik)
            self.timer_kom2.timeout.connect(self.timer_kom2.stop)
            self.timer_kom2.start(2000)

        self.UI.label_przedrostek.setText(self.data_pomiaru)

        self.UI.comboBox_kanaly0.activated['int'].connect(self.zmiana_kanal0)
        self.UI.comboBox_kanaly1.activated['int'].connect(self.zmiana_kanal1)
        self.UI.comboBox_kanaly2.activated['int'].connect(self.zmiana_kanal2)
        
        self.UI.comboBox_zakres1.activated['int'].connect(self.zmiana_zakres_1)
        self.UI.comboBox_zakres2.activated['int'].connect(self.zmiana_zakres_2)

        self.UI.comboBox_osx1.activated['int'].connect(self.wykres_1.zmien_osx)
        self.UI.comboBox_osx2.activated['int'].connect(self.wykres_2.zmien_osx)

        self.UI.doubleSpinBox_czestotliowsc.valueChanged['double'].connect(self.zmiana_czestotliwosc)
        
        self.UI.nazwa_pliku.textChanged['QString'].connect(self.zmiana_nazwa)

        self.UI.horizontalSlider.valueChanged['int'].connect(self.zmiana_moc)
        self.UI.horizontalSlider.sliderReleased.connect(self.moc_do_arduino)

        self.UI.comboBox.activated['int'].connect(self.UI.stackedWidget.setCurrentIndex)

        self.UI.pushButton_start.clicked.connect(self.start_stop)
        self.UI.menuUstawienia.triggered.connect(self.open_dialog_ust)

        self.UI.menuPomoc.triggered.connect(self.open_dialog_pom)
        self.UI.menuPomoc.triggered.connect(self.miernik.ustaw_r)

        self.UI.pushButton_2.clicked.connect(self.reset)

    def start_stop(self):
        self.UI.comboBox.setEnabled(False)
        self.UI.nazwa_pliku.setEnabled(False)
        self.licznik_start()

        if( self.pomiar_start == 0):
            self.pomiar_start=1
            self.UI.pushButton_start.setText("Stop")
            self.UI.pushButton_2.setEnabled(False)
            self.pomiar()
        else:
            self.pomiar_start=0
            self.UI.pushButton_start.setText("Start")
            self.UI.pushButton_2.setEnabled(True)
            self.timer_out.stop()
        
        if(self.uruchomiono==0):
            self.czas_0=time.time() 
            # self.zapis_surowe()
            self.zapis_prztworzone("Czas 1. [s]","Temperatura 1. [K]","Opór 1. [Ohm]","Czas 2. [s]","Temperatura 2. [K]","Opór 2. [Ohm]")
            self.uruchomiono=1

    def rysuj(self):
        self.przetworz()
        self.poprzednia_temperatura=self.obecna_temperatura
        self.obecna_temperatura=self.dane_raw[3,1]
        self.tempo_przyrostu=(self.obecna_temperatura-self.poprzednia_temperatura)/self.czestotliwosc*60
        self.UI.label_aktualna_temp_wartosc.setText(str(round(self.obecna_temperatura,2)))
        self.UI.label_srednie_tempo.setText(str(round(self.tempo_przyrostu,2)))

        self.zapis_prztworzone(self.dane_przetworzone[0,0],self.dane_przetworzone[0,1],self.dane_przetworzone[0,2],self.dane_przetworzone[1,0],self.dane_przetworzone[1,1],self.dane_przetworzone[1,2])
        self.zapis_surowe(self.dane_raw[0,0],self.dane_raw[0,1],self.dane_raw[1,0],self.dane_raw[1,1],self.dane_raw[2,0],self.dane_raw[2,1],self.dane_raw[3,0],self.dane_raw[3,1])
        
        self.wykres_0.dane=np.append(self.wykres_0.dane,[[ self.dane_raw[3,0],self.dane_raw[3,1]]],axis=0)
        self.wykres_1.dane=np.append(self.wykres_1.dane,[self.dane_przetworzone[0]],axis=0)
        self.wykres_2.dane=np.append(self.wykres_2.dane,[self.dane_przetworzone[1]],axis=0)
        self.wykres_0.update_figure()
        self.wykres_1.update_figure()
        self.wykres_2.update_figure()

    def przetworz(self):
        a=(self.dane_raw[0,1]-self.dane_raw[3,1])/(self.dane_raw[0,0]-self.dane_raw[3,0])
        b=self.dane_raw[0,1]-a*self.dane_raw[0,0]

        self.dane_przetworzone[0,0]=self.dane_raw[1,0]
        self.dane_przetworzone[0,1]=a*self.dane_raw[1,0]+b
        self.dane_przetworzone[0,2]=self.dane_raw[1,1]
        self.dane_przetworzone[1,0]=self.dane_raw[2,0]
        self.dane_przetworzone[1,1]=a*self.dane_raw[2,0]+b
        self.dane_przetworzone[1,2]=self.dane_raw[2,1]


    def reset(self):
        self.p1=0
        self.p2=0

        self.czestotliwosc=5
        self.obecna_temperatura=0
        self.poprzednia_temperatura=0
        self.tempo_przyrostu=0

        self.zakres_0=1000
        self.zakres_1=1000000
        self.zakres_2=100000000


        f = open('konfiguracja.json')
        data = json.load(f)
        self.plik_wyjsciowy= data['nazwa_pliku']
        self.sciezka=data['sciezka_zapisu']
        self.zapis_on=data['zapis']
        self.zakres_0=data['zakres_Pt100']

        f.close()

        self.data_pomiaru = time.strftime("%d_%m_%Y_", time.localtime())

        self.kanaly=[1,2,3]
        self.dane_raw=np.zeros([4,2])
        self.dane_przetworzone=np.zeros([2,3])

        self.uruchomiono=0
        self.pomiar_start=0
        self.czas_0=0
        self.UI.label_licznik.setText("00:00")
        
        self.wykres_0.reset_wykres()
        self.wykres_1.reset_wykres()
        self.wykres_2.reset_wykres()

        self.UI.comboBox.setEnabled(True)
        self.UI.nazwa_pliku.setEnabled(True)
        self.UI.doubleSpinBox_sledzenie.setEnabled(False)

        self.UI.label_srednie_tempo.setText("0")
        self.UI.label_aktualna_temp_wartosc.setText("0")
        self.UI.comboBox_kanaly0.setCurrentIndex(0)
        self.UI.comboBox_kanaly1.setCurrentIndex(1)
        self.UI.comboBox_kanaly2.setCurrentIndex(2)
        self.UI.comboBox_zakres1.setCurrentIndex(6)
        self.UI.comboBox_zakres2.setCurrentIndex(8)
        

        self.UI.nazwa_pliku.setText("")
        self.UI.label_tytul2.setText("Nazwa_pomiaru")

    def licznik_start(self):
        self.timer_licznik = QtCore.QTimer()
        if(self.pomiar_start==0):
            self.timer_licznik.timeout.connect(self.licznik_odswierz)
            self.timer_licznik.start(1000)
        if(self.pomiar_start==1):
            self.timer_licznik.stop()
        
    def licznik_odswierz(self):
        czas= round(time.time() - self.czas_0)
        s1=czas%60
        m1=round((czas-s1)/60)
        m2=str(m1)
        if(s1<10):
            s2="0"+str(s1)
        else:
            s2=str(s1)
        self.UI.label_licznik.setText(m2+":"+s2)
        
    def zmiana_moc(self,w):
        self.moc=w
        self.UI.label_aktualna_moc_wartosc.setText(str(self.moc))

    def zmiana_czestotliwosc(self,f):
        self.czestotliwosc=f
    
    def zmiana_zakres_0(self,f):
        self.zakres_0=f

    def zmiana_zakres_1(self,f):
        self.zakres_1=10**f

    def zmiana_zakres_2(self,f):
        self.zakres_2=10**f

    def moc_do_arduino(self):
        self.arduino.zmien_moc(self.moc)

    def zmiana_kanal0(self,ch):
        self.kanaly[0]=ch+1

    def zmiana_kanal1(self,ch):
        self.kanaly[1]=ch+1

    def zmiana_kanal2(self,ch):
        self.kanaly[2]=ch+1

    def zmiana_nazwa(self,n):
        self.plik_wyjsciowy=self.data_pomiaru+n
        self.UI.label_tytul2.setText(n)

    def zapis_prztworzone(self,t1,T1,R1,t2,T2,R2):
        with open(self.sciezka+self.plik_wyjsciowy+"_przetworzne.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( [t1,T1,R1,t2,T2,R2])

    def zapis_surowe(self,t0,R_temp_pocz,t1,R1,t2,R2,t3,R_temp_kon):
        with open(self.sciezka + self.plik_wyjsciowy+"_surowe.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( [t0,R_temp_pocz,t1,R1,t2,R2,t3,R_temp_kon])

    def pomiar(self):
        self.timer_out = QtCore.QTimer()
        self.pomiar_in_a()
        self.timer_out.timeout.connect(self.pomiar_in_a)
        self.timer_out.start(1000*self.czestotliwosc)

    def pomiar_in_a(self):
        self.p1=0
        self.p2=0
        self.timer_in = QtCore.QTimer()
        self.pomiar_in_b()
        self.timer_in.timeout.connect(self.pomiar_in_b)
        self.timer_in.start(400)

    def pomiar_in_b(self):
        if(self.p1<4):
            if(self.p2==0):
                self.miernik.zamknij(self.kanaly[self.p1%3])
                self.p2=1
            else:
                if(self.p1==0 or self.p1==3):
                    self.dane_raw[self.p1,0]=time.time()-self.czas_0
                    self.miernik.miernik.write(f"CONF:RES {self.zakres_0}")
                    self.dane_raw[self.p1,1]=(float(self.miernik.mierz())-self.B)/self.A                    
                elif(self.p1==1):
                    self.dane_raw[self.p1,0]=time.time()-self.czas_0
                    self.miernik.miernik.write(f"CONF:RES {self.zakres_1}")
                    self.dane_raw[self.p1,1]=self.miernik.mierz()
                else:
                    self.dane_raw[self.p1,0]=time.time()-self.czas_0
                    self.miernik.miernik.write(f"CONF:RES {self.zakres_2}")
                    self.dane_raw[self.p1,1]=self.miernik.mierz()
                self.p1+=1
                self.p2=0
        else:
            self.rysuj()
            self.timer_in.stop()
        
    def open_dialog_ust(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Form1()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()
    
    def open_dialog_pom(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Form2()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def komunikat_grzalka(self):
        msg =QMessageBox()
        msg.setWindowTitle("Ostrzeżenie")
        msg.setText("Zasilacz grzałki nie jest podłączony do komutera, czy chcesz kontynuować bez możliwoaści sterowania mocą grzałki?")
        msg.setIcon(QMessageBox.Warning)
        x=msg.exec_()

    def komunikat_miernik(self):
        msg =QMessageBox()
        msg.setWindowTitle("Ostrzeżenie")
        msg.setText("Miernik nie jest podłączony do komputera, wykonywanie pomiarów nie będzie możliwe.")
        msg.setIcon(QMessageBox.Critical)
        x=msg.exec_()

