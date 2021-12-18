from interfejs import Ui_MainWindow
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

        self.set_zmienne()
        self.set_polaczenia()

    def set_zmienne(self):
        self.P2_wykres_t = wykres.Wykres_temp(self.UI.P2_okno_wykresu_t,width=450/90,height=270/90, dpi=90)
        self.P2_wykres_p1 = wykres.Wykres_probka(self.UI.P2_okno_wykresu_p1,width=530/90,height=310/90, dpi=90)
        self.P2_wykres_p2 = wykres.Wykres_probka(self.UI.P2_okno_wykresu_p2,width=530/90,height=310/90, dpi=90)
        self.R4_wykres_t = wykres.Wykres_temp(self.UI.R4_okno_wykresu_t,width=410/90,height=260/90, dpi=90)
        self.R4_wykres_p2 = wykres.Wykres_probka(self.UI.R4_okno_wykresu_p,width=660/90,height=600/90, dpi=90)
        self.CH20_wykres_p2 = wykres.Wykres_probka(self.UI.CH20_okno_wykresu,width=680/90,height=610/90, dpi=90)

        self.arduino=grzalka.Grzanie()

        if(self.arduino.error==1):
            self.UI.P2_moc_suwak.setEnabled(False)  
            self.timer_komunikat1 = QtCore.QTimer()
            self.timer_komunikat1.timeout.connect(self.komunikat_grzalka)
            self.timer_komunikat1.timeout.connect(self.timer_komunikat1.stop)
            self.timer_komunikat1.start(1000)

        self.miernik=miernik20.Aparature()
        if(self.miernik.error==1):
            self.UI.P2_start.setEnabled(False)
            self.UI.R4_start.setEnabled(False)
            self.UI.CH20_start.setEnabled(False)
   
            self.timer_komunikat2 = QtCore.QTimer()
            self.timer_komunikat2.timeout.connect(self.komunikat_miernik)
            self.timer_komunikat2.timeout.connect(self.timer_komunikat2.stop)
            self.timer_komunikat2.start(2000)

        self.data_pomiaru = time.strftime("%d_%m_%Y_", time.localtime())
        self.UI.nazwa_pliku_przedrostek.setText(self.data_pomiaru)

        self.p1=0
        self.p2=0        
        
        self.czestotliwosc=5
        self.obecna_temperatura=0
        self.poprzednia_temperatura=0
        self.tempo_przyrostu=0
        
        self.zakres_t=1000
        self.P2_zakres_p1=1000000
        self.P2_zakres_p2=100000000

        self.zakres_t=1000
        self.R4_zakres_p=100

        f = open('konfiguracja.json')
        data = json.load(f)
        self.plik_wyjsciowy= data['nazwa_pliku']
        self.sciezka=data['sciezka_zapisu']
        self.zapis_on=data['zapis']
        self.zakres_t=data['zakres_Pt100']
        self.A=0.385
        self.B=5.15
        f.close()

        self.kanaly=[1,2,3]
        self.dane_raw=np.zeros([4,2])
        self.dane_przetworzone=np.zeros([2,3])

        self.uruchomiono=0
        self.pomiar_start=0

        self.UI.P2_sledzenie_temp_wartosc.setEnabled(False)
        self.UI.R4_sledzenie_temp_wartosc.setEnabled(False)

        self.UI.P2_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.P2_wybor_kanalow_p1.setCurrentIndex(1)
        self.UI.P2_wybor_kanalow_p2.setCurrentIndex(2)
        self.UI.P2_zakres_p1.setCurrentIndex(6)
        self.UI.P2_zakres_p2.setCurrentIndex(8)
        
        self.UI.R4_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.R4_wybor_kanalow_p.setCurrentIndex(3)
        self.UI.R4_zakres_p.setCurrentIndex(2)

        self.UI.nazwa_pliku.setText("")

    def set_polaczenia(self):
        #ogólne
        self.UI.nazwa_pliku.textChanged['QString'].connect(self.zmiana_nazwa)
        self.UI.zmiana_trybu.activated['int'].connect(self.UI.stackedWidget.setCurrentIndex)
        self.UI.Ustawienia.triggered.connect(self.open_dialog_ust)
        self.UI.Pomoc.triggered.connect(self.open_dialog_pom)
        #pomiar 2 próbek 
        self.UI.P2_wybor_kanalow_t.activated['int'].connect(self.zmiana_kanal0)
        self.UI.P2_wybor_kanalow_p1.activated['int'].connect(self.zmiana_kanal1)
        self.UI.P2_wybor_kanalow_p2.activated['int'].connect(self.zmiana_kanal2)

        self.UI.P2_zakres_p1.activated['int'].connect(self.P2_zmiana_zakres_p1)
        self.UI.P2_zakres_p2.activated['int'].connect(self.P2_zmiana_zakres_p2)

        self.UI.P2_wybor_osix_p1.activated['int'].connect(self.P2_wykres_p1.zmien_osx)
        self.UI.P2_wybor_osix_p2.activated['int'].connect(self.P2_wykres_p2.zmien_osx)

        self.UI.P2_czestotliowsc.valueChanged['double'].connect(self.zmiana_czestotliwosc)

        self.UI.P2_moc_suwak.valueChanged['int'].connect(self.zmiana_moc)
        self.UI.P2_moc_suwak.sliderReleased.connect(self.moc_do_arduino)

        self.UI.P2_start.clicked.connect(self.P2_start_stop)

        self.UI.P2_reset.clicked.connect(self.reset)

        #pomiar 4-punktowy
        self.UI.R4_wybor_kanalow_t.activated['int'].connect(self.zmiana_kanal0)
        self.UI.R4_wybor_kanalow_p.activated['int'].connect(self.zmiana_kanal1)

        self.UI.R4_zakres_p.activated['int'].connect(self.R4_zmiana_zakres_p)

        self.UI.R4_wybor_osix_p.activated['int'].connect(self.P2_wykres_p1.zmien_osx)

        self.UI.R4_moc_suwak.valueChanged['int'].connect(self.zmiana_moc)
        self.UI.R4_moc_suwak.sliderReleased.connect(self.moc_do_arduino)

        # self.UI.R4_start.clicked.connect(self.R4_start_stop)

        self.UI.R4_reset.clicked.connect(self.reset)

    def reset(self):
        self.p1=0
        self.p2=0

        self.czestotliwosc=5
        self.obecna_temperatura=0
        self.poprzednia_temperatura=0
        self.tempo_przyrostu=0

        self.zakres_t=1000
        self.P2_zakres_p1=1000000
        self.P2_zakres_p2=100000000

        f = open('konfiguracja.json')
        data = json.load(f)
        self.plik_wyjsciowy= data['nazwa_pliku']
        self.sciezka=data['sciezka_zapisu']
        self.zapis_on=data['zapis']
        self.zakres_t=data['zakres_Pt100']
        self.A=0.385
        self.B=5.15
        f.close()

        self.kanaly=[1,2,3]
        self.dane_raw=np.zeros([4,2])
        self.dane_przetworzone=np.zeros([2,3])

        self.uruchomiono=0
        self.pomiar_start=0
        self.czas_0=0
        self.UI.P2_licznik.setText("00:00")
        
        self.P2_wykres_t.reset_wykres()
        self.P2_wykres_p1.reset_wykres()
        self.P2_wykres_p2.reset_wykres()

        self.UI.zmiana_trybu.setEnabled(True)
        self.UI.nazwa_pliku.setEnabled(True)
        self.UI.P2_sledzenie_temp_wartosc.setEnabled(False)

        self.UI.P2_tempo.setText("0")
        self.UI.P2_temperatura.setText("0")
        self.UI.P2_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.P2_wybor_kanalow_p1.setCurrentIndex(1)
        self.UI.P2_wybor_kanalow_p2.setCurrentIndex(2)
        self.UI.P2_zakres_p1.setCurrentIndex(6)
        self.UI.P2_zakres_p2.setCurrentIndex(8)
        
        self.UI.nazwa_pliku.setText("")
        self.UI.naglowek.setText("Nazwa_pomiaru")

#pomiar 2 próbek
    def P2_start_stop(self):
        self.UI.zmiana_trybu.setEnabled(False)
        self.UI.nazwa_pliku.setEnabled(False)
        self.licznik_start()

        if( self.pomiar_start == 0):
            self.pomiar_start=1
            self.UI.P2_start.setText("Stop")
            self.UI.P2_reset.setEnabled(False)
            self.pomiar()
        else:
            self.pomiar_start=0
            self.UI.P2_start.setText("Start")
            self.UI.P2_reset.setEnabled(True)
            self.timer_out.stop()
        
        if(self.uruchomiono==0):
            self.czas_0=time.time()
            self.zapis_prztworzone("Czas 1. [s]","Temperatura 1. [K]","Opór 1. [Ohm]","Czas 2. [s]","Temperatura 2. [K]","Opór 2. [Ohm]")
            self.uruchomiono=1

    def P2_rysuj(self):
        self.P2_wykres_t.dane=np.append(self.P2_wykres_t.dane,[[ self.dane_raw[3,0],self.dane_raw[3,1]]],axis=0)
        self.P2_wykres_p1.dane=np.append(self.P2_wykres_p1.dane,[self.dane_przetworzone[0]],axis=0)
        self.P2_wykres_p2.dane=np.append(self.P2_wykres_p2.dane,[self.dane_przetworzone[1]],axis=0)
        self.P2_wykres_t.update_figure()
        self.P2_wykres_p1.update_figure()
        self.P2_wykres_p2.update_figure()

    def P2_przetworz(self):
        a=(self.dane_raw[0,1]-self.dane_raw[3,1])/(self.dane_raw[0,0]-self.dane_raw[3,0])
        b=self.dane_raw[0,1]-a*self.dane_raw[0,0]

        self.dane_przetworzone[0,0]=self.dane_raw[1,0]
        self.dane_przetworzone[0,1]=a*self.dane_raw[1,0]+b
        self.dane_przetworzone[0,2]=self.dane_raw[1,1]
        self.dane_przetworzone[1,0]=self.dane_raw[2,0]
        self.dane_przetworzone[1,1]=a*self.dane_raw[2,0]+b
        self.dane_przetworzone[1,2]=self.dane_raw[2,1]

        self.poprzednia_temperatura=self.obecna_temperatura
        self.obecna_temperatura=self.dane_raw[3,1]
        self.tempo_przyrostu=(self.obecna_temperatura-self.poprzednia_temperatura)/self.czestotliwosc*60
        self.UI.P2_temperatura.setText(str(round(self.obecna_temperatura,2)))
        self.UI.P2_tempo.setText(str(round(self.tempo_przyrostu,2)))

    def P2_zapisz(self):
        self.zapis_prztworzone(self.dane_przetworzone[0,0],self.dane_przetworzone[0,1],self.dane_przetworzone[0,2],self.dane_przetworzone[1,0],self.dane_przetworzone[1,1],self.dane_przetworzone[1,2])
        self.zapis_surowe(self.dane_raw[0,0],self.dane_raw[0,1],self.dane_raw[1,0],self.dane_raw[1,1],self.dane_raw[2,0],self.dane_raw[2,1],self.dane_raw[3,0],self.dane_raw[3,1])
        
    def P2_zmiana_zakres_p1(self,f):
        self.P2_zakres_p1=10**f

    def P2_zmiana_zakres_p2(self,f):
        self.P2_zakres_p2=10**f

    def zmiana_kanal0(self,ch):
        self.kanaly[0]=ch+1

    def zmiana_kanal1(self,ch):
        self.kanaly[1]=ch+1

    def zmiana_kanal2(self,ch):
        self.kanaly[2]=ch+1

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
                    self.miernik.miernik.write(f"CONF:RES {self.zakres_t}")
                    self.dane_raw[self.p1,1]=(float(self.miernik.mierz())-self.B)/self.A                    
                elif(self.p1==1):
                    self.dane_raw[self.p1,0]=time.time()-self.czas_0
                    self.miernik.miernik.write(f"CONF:RES {self.P2_zakres_p1}")
                    self.dane_raw[self.p1,1]=self.miernik.mierz()
                else:
                    self.dane_raw[self.p1,0]=time.time()-self.czas_0
                    self.miernik.miernik.write(f"CONF:RES {self.P2_zakres_p2}")
                    self.dane_raw[self.p1,1]=self.miernik.mierz()
                self.p1+=1
                self.p2=0
        else:
            self.P2_przetworz()
            self.P2_zapisz()
            self.P2_rysuj()
            self.timer_in.stop()

#------------

#pomiar 4-punktowy
    def R4_zmiana_zakres_p(self,f):
        self.R4_zakres_p=10**f
#---------

#pomiar ręczny

#------

#ogólne
    def zmiana_nazwa(self,n):
        self.plik_wyjsciowy=self.data_pomiaru+n
        self.UI.naglowek.setText(n)

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
        self.UI.P2_licznik.setText(m2+":"+s2)
        self.UI.R4_licznik.setText(m2+":"+s2)


    def zmiana_moc(self,w):
        self.moc=w
        self.UI.P2_moc.setText(str(self.moc))
        self.UI.R4_moc.setText(str(self.moc))

    def zmiana_czestotliwosc(self,f):
        self.czestotliwosc=f
    
    def zmiana_zakres_t(self,f):
        self.zakres_t=f

    def moc_do_arduino(self):
        self.arduino.zmien_moc(self.moc)

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

#