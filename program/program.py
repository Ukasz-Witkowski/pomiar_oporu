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
     #ogólne
        self.arduino=grzalka.Grzanie()
        if(self.arduino.error==1):
            self.UI.P2_moc_suwak.setEnabled(False)  
            self.UI.R4_moc_suwak.setEnabled(False)  
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

        self.uruchomiono=0
        self.pomiar_start=0
        self.automatyczna_temperatura=250
        self.sledzenie_ok=0

        self.zakres_t=1000
        self.obecna_temperatura=0
        self.poprzednia_temperatura=0
        self.tempo_przyrostu=0

        f = open('konfiguracja.json')
        data = json.load(f)
        self.plik_wyjsciowy= data['nazwa_pliku']
        self.sciezka=data['sciezka_zapisu']
        self.zapis_on=data['zapis']
        self.zakres_t=data['zakres_Pt100']
        self.A=0.385
        self.B=5.15
        f.close()

        self.UI.nazwa_pliku.setText("")
     #---------

     #pomiar 2 próbek
        self.P2_wykres_t = wykres.Wykres_temp(self.UI.P2_okno_wykresu_t,width=450/90,height=270/90, dpi=90)
        self.P2_wykres_p1 = wykres.Wykres_probka(self.UI.P2_okno_wykresu_p1,width=530/90,height=310/90, dpi=90)
        self.P2_wykres_p2 = wykres.Wykres_probka(self.UI.P2_okno_wykresu_p2,width=530/90,height=310/90, dpi=90)

        self.P2_czestotliwosc=5

        self.P2_zakres_p1=1000000
        self.P2_zakres_p2=100000000

        self.P2_kanaly=[1,2,3]

        self.P2_dane_surowe=np.zeros([4,2])
        self.P2_dane_przetworzone=np.zeros([2,3])
        
        # self.UI.P2_sledzenie_temp_wartosc.setEnabled(False)
        self.UI.P2_sledzenie_temp_wartosc.setValue(250)


        self.UI.P2_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.P2_wybor_kanalow_p1.setCurrentIndex(1)
        self.UI.P2_wybor_kanalow_p2.setCurrentIndex(2)
        self.UI.P2_zakres_p1.setCurrentIndex(4)
        self.UI.P2_zakres_p2.setCurrentIndex(6)
     #------------
       
     #pomiar 4-punktowy  
        self.R4_wykres_t = wykres.Wykres_temp(self.UI.R4_okno_wykresu_t,width=410/90,height=270/90, dpi=90)
        self.R4_wykres_p = wykres.Wykres_probka(self.UI.R4_okno_wykresu_p,width=660/90,height=630/90, dpi=90)
        
        self.R4_czestotliwosc=5

        self.R4_zakres_p=100

        self.R4_kanaly=[1,4]

        self.R4_dane_surowe=np.zeros([3,2])
        self.R4_dane_przetworzone=np.zeros([1,3])

        # self.UI.R4_sledzenie_temp_wartosc.setEnabled(False)     
        self.UI.R4_sledzenie_temp_wartosc.setValue(250)

        self.UI.R4_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.R4_wybor_kanalow_p.setCurrentIndex(3)
        self.UI.R4_zakres_p.setCurrentIndex(0)
     #-------

     #tryb reczny
        self.CH20_wykres = wykres.Wykres_20kanal(self.UI.CH20_okno_wykresu,width=680/90,height=610/90, dpi=90)
        
        self.CH20_czestotliwosc_in=3
        self.CH20_czestotliwosc_out=10

        self.CH20_dane_surowe=[[0 for x in range(40)]]

     #------------
    def set_polaczenia(self):
        #ogólne
        self.UI.nazwa_pliku.textChanged['QString'].connect(self.zmiana_nazwa)
        self.UI.zmiana_trybu.activated['int'].connect(self.UI.stackedWidget.setCurrentIndex)
        self.UI.Ustawienia.triggered.connect(self.open_dialog_ust)
        self.UI.Pomoc.triggered.connect(self.open_dialog_pom)
        #pomiar 2 próbek 
        self.UI.P2_wybor_kanalow_t.activated['int'].connect(self.P2_zmiana_kanal_t)
        self.UI.P2_wybor_kanalow_p1.activated['int'].connect(self.P2_zmiana_kanal_p1)
        self.UI.P2_wybor_kanalow_p2.activated['int'].connect(self.P2_zmiana_kanal_p2)

        self.UI.P2_zakres_p1.activated['int'].connect(self.P2_zmiana_zakres_p1)
        self.UI.P2_zakres_p2.activated['int'].connect(self.P2_zmiana_zakres_p2)

        self.UI.P2_wybor_osix_p1.activated['int'].connect(self.P2_wykres_p1.zmien_osx)
        self.UI.P2_wybor_osix_p2.activated['int'].connect(self.P2_wykres_p2.zmien_osx)

        self.UI.P2_czestotliowsc.valueChanged['double'].connect(self.P2_zmiana_czestotliwosc)

        self.UI.P2_moc_suwak.valueChanged['int'].connect(self.zmiana_moc)
        self.UI.P2_moc_suwak.sliderReleased.connect(self.moc_do_arduino)

        self.UI.P2_sledzenie_temp_okienko.toggled['bool'].connect(self.ustaw_sledzenie)
        self.UI.P2_sledzenie_temp_wartosc.valueChanged['double'].connect(self.zmien_automatyczna_temperatura)

        self.UI.P2_start.clicked.connect(self.P2_start_stop)

        self.UI.P2_reset.clicked.connect(self.reset)

        #pomiar 4-punktowy
        self.UI.R4_wybor_kanalow_t.activated['int'].connect(self.R4_zmiana_kanal_t)
        self.UI.R4_wybor_kanalow_p.activated['int'].connect(self.R4_zmiana_kanal_p)

        self.UI.R4_zakres_p.activated['int'].connect(self.R4_zmiana_zakres_p)

        self.UI.R4_wybor_osix_p.activated['int'].connect(self.R4_wykres_p.zmien_osx)

        self.UI.R4_moc_suwak.valueChanged['int'].connect(self.zmiana_moc)
        self.UI.R4_moc_suwak.sliderReleased.connect(self.moc_do_arduino)

        
        self.UI.R4_sledzenie_temp_okienko.toggled['bool'].connect(self.ustaw_sledzenie)
        self.UI.R4_sledzenie_temp_wartosc.valueChanged['double'].connect(self.zmien_automatyczna_temperatura)

        self.UI.R4_start.clicked.connect(self.R4_start_stop)

        self.UI.R4_reset.clicked.connect(self.reset)

        #20 próbek
        self.UI.CH20_czestotliowsc_in.valueChanged['double'].connect(self.CH20_zmiana_czestotliwosc_in)
        self.UI.CH20_czestotliowsc_out.valueChanged['double'].connect(self.CH20_zmiana_czestotliwosc_out)

        for i in range(20):
            eval("self.UI.checkBox_"+str(i+1)+".toggled['bool'].connect(self.CH20_kanal_ok"+str(i+1)+")")
            eval("self.UI.comboBox_"+str(i+1)+".activated['int'].connect(self.CH20_tryb"+str(i+1)+")")

        self.UI.CH20_start.clicked.connect(self.CH20_start_stop)
        self.UI.CH20_reset.clicked.connect(self.reset)

    def reset(self):
        #ogólne
        self.p1=0
        self.p2=0
        self.obecna_temperatura=0
        self.poprzednia_temperatura=0
        self.tempo_przyrostu=0
        self.zakres_t=1000
        
        f = open('konfiguracja.json')
        data = json.load(f)
        self.plik_wyjsciowy= data['nazwa_pliku']
        self.sciezka=data['sciezka_zapisu']
        self.zapis_on=data['zapis']
        self.zakres_t=data['zakres_Pt100']
        self.A=0.385
        self.B=5.15
        f.close()

        self.uruchomiono=0
        self.pomiar_start=0
        self.czas_0=0

        self.UI.zmiana_trybu.setEnabled(True)
        self.UI.nazwa_pliku.setEnabled(True)
        
        self.UI.nazwa_pliku.setText("")
        self.UI.naglowek.setText("Nazwa_pomiaru")
        #---------

        #pomiar 2 próbek
        self.P2_czestotliwosc=5
        self.UI.P2_czestotliowsc.setValue(5)

        self.P2_zakres_p1=1000000
        self.P2_zakres_p2=100000000

        self.P2_kanaly=[1,2,3]
        self.P2_dane_surowe=np.zeros([4,2])
        self.P2_dane_przetworzone=np.zeros([2,3])
        
        self.UI.P2_licznik.setText("00:00")
        
        self.P2_wykres_t.reset_wykres()
        self.P2_wykres_p1.reset_wykres()
        self.P2_wykres_p2.reset_wykres()

        self.UI.P2_tempo.setText("0")
        self.UI.P2_temperatura.setText("0")
        self.UI.P2_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.P2_wybor_kanalow_p1.setCurrentIndex(1)
        self.UI.P2_wybor_kanalow_p2.setCurrentIndex(2)
        self.UI.P2_zakres_p1.setCurrentIndex(6)
        self.UI.P2_zakres_p2.setCurrentIndex(8)

        self.UI.P2_sledzenie_temp_wartosc.setValue(250)
        # self.UI.P2_sledzenie_temp_wartosc.setEnabled(False)
        #-----------


        #pomiar 4-punktowy
        self.R4_czestotliwosc=5
        
        self.UI.R4_czestotliowsc.setValue(5)
        self.R4_zakres_p=100

        self.R4_kanaly=[1,4]
        self.P2_dane_surowe=np.zeros([4,2])
        self.P2_dane_przetworzone=np.zeros([2,3])
        
        self.UI.R4_licznik.setText("00:00")
        
        self.R4_wykres_t.reset_wykres()
        self.R4_wykres_p.reset_wykres()

        self.UI.R4_tempo.setText("0")
        self.UI.R4_temperatura.setText("0")
        self.UI.R4_wybor_kanalow_t.setCurrentIndex(0)
        self.UI.R4_wybor_kanalow_p.setCurrentIndex(3)
        self.UI.R4_zakres_p.setCurrentIndex(0)

        self.UI.R4_sledzenie_temp_wartosc.setValue(250)
        # self.UI.R4_sledzenie_temp_wartosc.setEnabled(False)
        #-----------
        
        #20 kanałów

        self.CH20_wykres = wykres.Wykres_20kanal(self.UI.CH20_okno_wykresu,width=680/90,height=610/90, dpi=90)
        
        self.CH20_czestotliwosc_in=3
        self.UI.CH20_czestotliowsc_in.setValue(3)

        self.CH20_czestotliwosc_out=10
        self.UI.CH20_czestotliowsc_out.setValue(10)

        self.CH20_dane_surowe=[[0 for x in range(40)]]

        
        self.UI.CH20_licznik.setText("00:00")
        
        self.CH20_wykres.reset_wykres()


        # 

#pomiar 2 próbek

    def P2_start_stop(self):
        self.UI.zmiana_trybu.setEnabled(False)
        self.UI.nazwa_pliku.setEnabled(False)
        self.licznik_start()

        if( self.pomiar_start == 0):
            self.pomiar_start=1
            self.UI.P2_start.setText("Stop")
            self.UI.P2_reset.setEnabled(False)
            self.P2_pomiar_out()
        else:
            self.pomiar_start=0
            self.UI.P2_start.setText("Start")
            self.UI.P2_reset.setEnabled(True)
            self.P2_timer_out.stop()
        
        if(self.uruchomiono==0):
            self.czas_0=time.time()
            self.P2_zapis_przetworzone("Czas 1. [s]","Temperatura 1. [K]","Opór 1. [Ohm]","Czas 2. [s]","Temperatura 2. [K]","Opór 2. [Ohm]")
            self.P2_zapis_surowe("Czas 1. [s]","Opór 1. [Ohm]","Czas 2. [s]","Opór 2. [Ohm]","Czas 3. [s]","Opór 3. [Ohm]","Czas 4.","Opór 4. [Ohm]")
            self.uruchomiono=1

    def P2_rysuj(self):
        self.P2_wykres_t.dane=np.append(self.P2_wykres_t.dane,[[ self.P2_dane_surowe[3,0],self.P2_dane_surowe[3,1]]],axis=0)
        self.P2_wykres_p1.dane=np.append(self.P2_wykres_p1.dane,[self.P2_dane_przetworzone[0]],axis=0)
        self.P2_wykres_p2.dane=np.append(self.P2_wykres_p2.dane,[self.P2_dane_przetworzone[1]],axis=0)
        self.P2_wykres_t.update_figure()
        self.P2_wykres_p1.update_figure()
        self.P2_wykres_p2.update_figure()

    def P2_przetworz(self):
        a=(self.P2_dane_surowe[0,1]-self.P2_dane_surowe[3,1])/(self.P2_dane_surowe[0,0]-self.P2_dane_surowe[3,0])
        b=self.P2_dane_surowe[0,1]-a*self.P2_dane_surowe[0,0]

        self.P2_dane_przetworzone[0,0]=self.P2_dane_surowe[1,0]
        self.P2_dane_przetworzone[0,1]=a*self.P2_dane_surowe[1,0]+b
        self.P2_dane_przetworzone[0,2]=self.P2_dane_surowe[1,1]
        self.P2_dane_przetworzone[1,0]=self.P2_dane_surowe[2,0]
        self.P2_dane_przetworzone[1,1]=a*self.P2_dane_surowe[2,0]+b
        self.P2_dane_przetworzone[1,2]=self.P2_dane_surowe[2,1]

        self.poprzednia_temperatura=self.obecna_temperatura
        self.obecna_temperatura=self.P2_dane_surowe[3,1]
        self.tempo_przyrostu=(self.obecna_temperatura-self.poprzednia_temperatura)/self.P2_czestotliwosc*60

        if(self.sledzenie_ok==1):
            roznica=(self.automatyczna_temperatura-self.obecna_temperatura)
            if(roznica<0):
                moc=0
            if(roznica>=0 and roznica<=5):
                if(self.tempo_przyrostu<0):
                    moc=50
                if(self.tempo_przyrostu>=0 and self.tempo_przyrostu<1):
                    moc=30
                if(self.tempo_przyrostu>=1 and self.tempo_przyrostu<3):
                    moc=20
                if(self.tempo_przyrostu>=3):
                    moc=5
            if( roznica>5 and roznica<=50 ):
                moc=50
            if(roznica>50):
                moc=100
            self.zmiana_moc(moc)
            self.moc_do_arduino()

        self.UI.P2_temperatura.setText(str(round(self.obecna_temperatura,2)))
        self.UI.P2_tempo.setText(str(round(self.tempo_przyrostu,2)))

    def P2_zapisz(self):
        self.P2_zapis_przetworzone(self.P2_dane_przetworzone[0,0],self.P2_dane_przetworzone[0,1],self.P2_dane_przetworzone[0,2],self.P2_dane_przetworzone[1,0],self.P2_dane_przetworzone[1,1],self.P2_dane_przetworzone[1,2])
        self.P2_zapis_surowe(self.P2_dane_surowe[0,0],self.P2_dane_surowe[0,1],self.P2_dane_surowe[1,0],self.P2_dane_surowe[1,1],self.P2_dane_surowe[2,0],self.P2_dane_surowe[2,1],self.P2_dane_surowe[3,0],self.P2_dane_surowe[3,1])
        
    def P2_zmiana_zakres_p1(self,f):
        self.P2_zakres_p1=10**(f+2)

    def P2_zmiana_zakres_p2(self,f):
        self.P2_zakres_p2=10**(f+2)

    def P2_zmiana_kanal_t(self,ch):
        self.P2_kanaly[0]=ch+1

    def P2_zmiana_kanal_p1(self,ch):
        self.P2_kanaly[1]=ch+1

    def P2_zmiana_kanal_p2(self,ch):
        self.P2_kanaly[2]=ch+1

    def P2_zmiana_czestotliwosc(self,f):
        self.P2_czestotliwosc=f
    
    def P2_zapis_przetworzone(self,t1,T1,R1,t2,T2,R2):
        with open(self.sciezka+self.plik_wyjsciowy+"_przetworzne.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( [t1,T1,R1,t2,T2,R2])

    def P2_zapis_surowe(self,t0,R_temp_pocz,t1,R1,t2,R2,t3,R_temp_kon):
        with open(self.sciezka + self.plik_wyjsciowy+"_surowe.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( [t0,R_temp_pocz,t1,R1,t2,R2,t3,R_temp_kon])

    def P2_pomiar_out(self):
        self.P2_timer_out = QtCore.QTimer()
        self.P2_pomiar_in_a()
        self.P2_timer_out.timeout.connect(self.P2_pomiar_in_a)
        self.P2_timer_out.start(1000*self.P2_czestotliwosc)

    def P2_pomiar_in_a(self):
        self.p1=0
        self.p2=0
        self.P2_timer_in = QtCore.QTimer()
        self.P2_pomiar_in_b()
        self.P2_timer_in.timeout.connect(self.P2_pomiar_in_b)
        self.P2_timer_in.start(400)

    def P2_pomiar_in_b(self):
        if(self.p1<4):
            if(self.p2==0):
                self.miernik.zamknij(self.P2_kanaly[self.p1%3])
                self.p2=1
            else:
                if(self.p1==0 or self.p1==3):
                    self.P2_dane_surowe[self.p1,0]=time.time()-self.czas_0
                    self.miernik.ustaw_r_zakres(self.zakres_t)
                    self.P2_dane_surowe[self.p1,1]=(float(self.miernik.mierz())-self.B)/self.A                    
                elif(self.p1==1):
                    self.P2_dane_surowe[self.p1,0]=time.time()-self.czas_0
                    self.miernik.ustaw_r_zakres(self.P2_zakres_p1)
                    self.P2_dane_surowe[self.p1,1]=self.miernik.mierz()
                else:
                    self.P2_dane_surowe[self.p1,0]=time.time()-self.czas_0
                    self.miernik.ustaw_r_zakres(self.P2_zakres_p2)
                    self.P2_dane_surowe[self.p1,1]=self.miernik.mierz()
                self.p1+=1
                self.p2=0
        else:
            self.P2_przetworz()
            self.P2_zapisz()
            self.P2_rysuj()
            self.P2_timer_in.stop()

#------------

#pomiar 4-punktowy    
    def R4_start_stop(self):
        self.UI.zmiana_trybu.setEnabled(False)
        self.UI.nazwa_pliku.setEnabled(False)
        self.licznik_start()

        if( self.pomiar_start == 0):
            self.pomiar_start=1
            self.UI.R4_start.setText("Stop")
            self.UI.R4_reset.setEnabled(False)
            self.R4_pomiar_out()
        else:
            self.pomiar_start=0
            self.UI.R4_start.setText("Start")
            self.UI.R4_reset.setEnabled(True)
            self.R4_timer_out.stop()
        
        if(self.uruchomiono==0):
            self.czas_0=time.time()
            self.R4_zapis_przetworzone("Czas [s]","Temperatura [K]","Opór [Ohm]")
            self.R4_zapis_surowe("Czas 1. [s]","Opór 1. [Ohm]","Czas 2. [s]","Opór 2. [Ohm]","Czas 3. [s]","Opór 3. [Ohm]")
            self.uruchomiono=1

    def R4_rysuj(self):
        self.R4_wykres_t.dane=np.append(self.R4_wykres_t.dane,[[ self.R4_dane_surowe[2,0],self.R4_dane_surowe[2,1]]],axis=0)
        self.R4_wykres_p.dane=np.append(self.R4_wykres_p.dane,[self.R4_dane_przetworzone[0]],axis=0)
        self.R4_wykres_t.update_figure()
        self.R4_wykres_p.update_figure()

    def R4_przetworz(self):
        a=(self.R4_dane_surowe[0,1]-self.R4_dane_surowe[2,1])/(self.R4_dane_surowe[0,0]-self.R4_dane_surowe[2,0])
        b=self.R4_dane_surowe[0,1]-a*self.R4_dane_surowe[0,0]

        self.R4_dane_przetworzone[0,0]=self.R4_dane_surowe[1,0]
        self.R4_dane_przetworzone[0,1]=a*self.R4_dane_surowe[1,0]+b
        self.R4_dane_przetworzone[0,2]=self.R4_dane_surowe[1,1]

        self.poprzednia_temperatura=self.obecna_temperatura
        self.obecna_temperatura=self.R4_dane_surowe[2,1]
        self.tempo_przyrostu=(self.obecna_temperatura-self.poprzednia_temperatura)/self.R4_czestotliwosc*60
        self.UI.R4_temperatura.setText(str(round(self.obecna_temperatura,2)))
        self.UI.R4_tempo.setText(str(round(self.tempo_przyrostu,2)))

    def R4_zapisz(self):
        self.R4_zapis_przetworzone(self.R4_dane_przetworzone[0,0],self.R4_dane_przetworzone[0,1],self.R4_dane_przetworzone[0,2])
        self.R4_zapis_surowe(self.R4_dane_surowe[0,0],self.R4_dane_surowe[0,1],self.R4_dane_surowe[1,0],self.R4_dane_surowe[1,1],self.R4_dane_surowe[2,0],self.R4_dane_surowe[2,1])
        
    def R4_zmiana_zakres_p(self,f):
        self.R4_zakres_p=10**(f+2)

    def R4_zmiana_kanal_t(self,ch):
        self.R4_kanaly[0]=ch+1

    def R4_zmiana_kanal_p(self,ch):
        self.R4_kanaly[1]=ch+1

    def R4_zmiana_czestotliwosc(self,f):
        self.R4_czestotliwosc=f
    
    def R4_zapis_przetworzone(self,t1,T1,R1):
        with open(self.sciezka+self.plik_wyjsciowy+"_przetworzne.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( [t1,T1,R1])

    def R4_zapis_surowe(self,t0,R_temp_pocz,t1,R1,t3,R_temp_kon):
        with open(self.sciezka + self.plik_wyjsciowy+"_surowe.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( [t0,R_temp_pocz,t1,R1,t3,R_temp_kon])

    def R4_pomiar_out(self):
        self.R4_timer_out = QtCore.QTimer()
        self.R4_pomiar_in_a()
        self.R4_timer_out.timeout.connect(self.R4_pomiar_in_a)
        self.R4_timer_out.start(1000*self.R4_czestotliwosc)

    def R4_pomiar_in_a(self):
        self.p1=0
        self.p2=0
        self.R4_timer_in = QtCore.QTimer()
        self.R4_pomiar_in_b()
        self.R4_timer_in.timeout.connect(self.R4_pomiar_in_b)
        self.R4_timer_in.start(400)

    def R4_pomiar_in_b(self):
        if(self.p1<3):
            if(self.p2==0):
                self.miernik.zamknij(self.R4_kanaly[self.p1%2])
                if(self.p1==1):
                    self.miernik.zamknij(self.R4_kanaly[self.p1%2])
                    self.miernik.ustaw_r4_zakres(self.R4_zakres_p)
                else:
                    self.miernik.ustaw_r_zakres(self.zakres_t)
                    
                self.p2=1
            else:
                if(self.p1==0 or self.p1==2):
                    self.R4_dane_surowe[self.p1,0]=time.time()-self.czas_0
                    self.R4_dane_surowe[self.p1,1]=(float(self.miernik.mierz())-self.B)/self.A                    
                else:
                    self.R4_dane_surowe[self.p1,0]=time.time()-self.czas_0
                    self.R4_dane_surowe[self.p1,1]=self.miernik.mierz()
                
                self.p1+=1
                self.p2=0
        else:
            self.R4_przetworz()
            self.R4_zapisz()
            self.R4_rysuj()
            self.R4_timer_in.stop()

#---------



#------20 kanałów--
    
    def CH20_kanal_ok1(self,a):
        self.CH20_wykres.tryb[0][0]=int(a)
    def CH20_kanal_ok2(self,a):
        self.CH20_wykres.tryb[0][1]=int(a)
    def CH20_kanal_ok3(self,a):
        self.CH20_wykres.tryb[0][2]=int(a)
    def CH20_kanal_ok4(self,a):
        self.CH20_wykres.tryb[0][3]=int(a)
    def CH20_kanal_ok5(self,a):
        self.CH20_wykres.tryb[0][4]=int(a)
    def CH20_kanal_ok6(self,a):
        self.CH20_wykres.tryb[0][5]=int(a)
    def CH20_kanal_ok7(self,a):
        self.CH20_wykres.tryb[0][6]=int(a)
    def CH20_kanal_ok8(self,a):
        self.CH20_wykres.tryb[0][7]=int(a)
    def CH20_kanal_ok9(self,a):
        self.CH20_wykres.tryb[0][8]=int(a)
    def CH20_kanal_ok10(self,a):
        self.CH20_wykres.tryb[0][9]=int(a)
    def CH20_kanal_ok11(self,a):
        self.CH20_wykres.tryb[0][10]=int(a)
    def CH20_kanal_ok12(self,a):
        self.CH20_wykres.tryb[0][11]=int(a)
    def CH20_kanal_ok13(self,a):
        self.CH20_wykres.tryb[0][12]=int(a)
    def CH20_kanal_ok14(self,a):
        self.CH20_wykres.tryb[0][13]=int(a)
    def CH20_kanal_ok15(self,a):
        self.CH20_wykres.tryb[0][14]=int(a)
    def CH20_kanal_ok16(self,a):
        self.CH20_wykres.tryb[0][15]=int(a)
    def CH20_kanal_ok17(self,a):
        self.CH20_wykres.tryb[0][16]=int(a)
    def CH20_kanal_ok18(self,a):
        self.CH20_wykres.tryb[0][17]=int(a)
    def CH20_kanal_ok19(self,a):
        self.CH20_wykres.tryb[0][18]=int(a)
    def CH20_kanal_ok20(self,a):
        self.CH20_wykres.tryb[0][19]=int(a)

    def CH20_tryb1(self,a):
        self.CH20_wykres.tryb[1][0]=int(a)
    def CH20_tryb2(self,a):
        self.CH20_wykres.tryb[1][1]=int(a)
    def CH20_tryb3(self,a):
        self.CH20_wykres.tryb[1][2]=int(a)
    def CH20_tryb4(self,a):
        self.CH20_wykres.tryb[1][3]=int(a)
    def CH20_tryb5(self,a):
        self.CH20_wykres.tryb[1][4]=int(a)
    def CH20_tryb6(self,a):
        self.CH20_wykres.tryb[1][5]=int(a)
    def CH20_tryb7(self,a):
        self.CH20_wykres.tryb[1][6]=int(a)
    def CH20_tryb8(self,a):
        self.CH20_wykres.tryb[1][7]=int(a)
    def CH20_tryb9(self,a):
        self.CH20_wykres.tryb[1][8]=int(a)
    def CH20_tryb10(self,a):
        self.CH20_wykres.tryb[1][9]=int(a)
    def CH20_tryb11(self,a):
        self.CH20_wykres.tryb[1][10]=int(a)
    def CH20_tryb12(self,a):
        self.CH20_wykres.tryb[1][11]=int(a)
    def CH20_tryb13(self,a):
        self.CH20_wykres.tryb[1][12]=int(a)
    def CH20_tryb14(self,a):
        self.CH20_wykres.tryb[1][13]=int(a)
    def CH20_tryb15(self,a):
        self.CH20_wykres.tryb[1][14]=int(a)
    def CH20_tryb16(self,a):
        self.CH20_wykres.tryb[1][15]=int(a)
    def CH20_tryb17(self,a):
        self.CH20_wykres.tryb[1][16]=int(a)
    def CH20_tryb18(self,a):
        self.CH20_wykres.tryb[1][17]=int(a)
    def CH20_tryb19(self,a):
        self.CH20_wykres.tryb[1][18]=int(a)
    def CH20_tryb20(self,a):
        self.CH20_wykres.tryb[1][19]=int(a)

    def CH20_start_stop(self):
        self.UI.zmiana_trybu.setEnabled(False)
        self.UI.nazwa_pliku.setEnabled(False)
        self.licznik_start()

        if( self.pomiar_start==0):
            self.pomiar_start=1
            self.UI.CH20_start.setText("Stop")
            self.UI.CH20_reset.setEnabled(False)
            self.CH20_pomiar_out()
        else:
            self.pomiar_start=0
            self.UI.CH20_start.setText("Start")
            self.UI.CH20_reset.setEnabled(True)
            self.CH20_timer_out.stop()
        
        if(self.uruchomiono==0):
            self.czas_0=time.time()
            # self.CH20_zapis_przetworzone_0()
            # self.CH20_zapis_surowe()
            self.uruchomiono=1

    def CH20_rysuj(self):
        print("fun rysuj")
        self.CH20_wykres.dane=np.append(self.CH20_wykres.dane,self.CH20_dane_surowe,axis=0)
        self.CH20_wykres.update_figure()


    def CH20_zapisz(self):
        print("fun zapisz")
        self.CH20_zapis_surowe(self.CH20_dane_surowe)

    def CH20_zmiana_czestotliwosc_in(self,f):
        self.CH20_czestotliwosc_in=f

    def CH20_zmiana_czestotliwosc_out(self,f):
        self.CH20_czestotliwosc_out=f

    def CH20_zapis_surowe(self, tab):

        with open(self.sciezka + self.plik_wyjsciowy+"_surowe.csv","a") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow( tab[0] )

    def CH20_pomiar_out(self):
        self.CH20_timer_out = QtCore.QTimer()
        self.CH20_pomiar_in_a()
        self.CH20_timer_out.timeout.connect(self.CH20_pomiar_in_a)
        self.CH20_timer_out.start(self.CH20_czestotliwosc_out*1000)

    def CH20_pomiar_in_a(self):
        self.p1=0
        self.p2=0
        self.CH20_timer_in = QtCore.QTimer()
        self.CH20_pomiar_in_b()
        self.CH20_timer_in.timeout.connect(self.CH20_pomiar_in_b)
        self.CH20_timer_in.start(self.CH20_czestotliwosc_in*500)

    def CH20_pomiar_in_b(self):
        print("bug1 p1="+str(self.p1)+" p2="+str(self.p2))

        while(self.CH20_wykres.tryb[0][self.p1]==0 and self.p1<19):
            print("bug2 p1="+str(self.p1)+" p2="+str(self.p2))
            self.p1+=1
        
        # print("bug3 p1="+str(self.p1)+" p2="+str(self.p2))
        # if(self.CH20_wykres.tryb[0][self.p1]==1):
        
        print("bug4 p1="+str(self.p1)+" p2="+str(self.p2))

        if(self.p2==0):
            print("bug5 p1="+str(self.p1)+" p2="+str(self.p2))
            self.miernik.zamknij(self.p1+1)
            self.p2=1
    
        else:
            print("bug6 p1="+str(self.p1)+" p2="+str(self.p2))
            if(self.CH20_wykres.tryb[1][self.p1]==0):
                print("bug7 p1="+str(self.p1)+" p2="+str(self.p2))
                self.miernik.ustaw_v()
                self.CH20_dane_surowe[0][self.p1*2-1]=float(self.miernik.mierz())                 
                self.CH20_dane_surowe[0][self.p1*2]=time.time()-self.czas_0
            else:
                print("bug8 p1="+str(self.p1)+" p2="+str(self.p2))
                self.miernik.ustaw_r()
                self.CH20_dane_surowe[0][self.p1*2-1]=float(self.miernik.mierz())     
                self.CH20_dane_surowe[0][self.p1*2]=time.time()-self.czas_0
            
            print("bug9 p1="+str(self.p1)+" p2="+str(self.p2))
            self.p1+=1
            
            while(self.CH20_wykres.tryb[0][self.p1]==0 and self.p1<19):
                print("bug12 p1="+str(self.p1)+" p2="+str(self.p2))
                self.p1+=1
            self.p2=0

        print("bug10 p1="+str(self.p1)+" p2="+str(self.p2))
        if(self.p1==19):
            print("bug11 p1="+str(self.p1)+" p2="+str(self.p2))
            self.CH20_zapisz()
            self.CH20_rysuj()
            self.CH20_timer_in.stop()

#------------


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
        self.UI.CH20_licznik.setText(m2+":"+s2)


    def zmiana_moc(self,w):
        self.moc=w
        self.UI.P2_moc.setText(str(self.moc))
        self.UI.R4_moc.setText(str(self.moc))

    def moc_do_arduino(self):
        print("moc: ",self.moc)
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
    def ustaw_sledzenie(self,s):
        if(s==1):
            self.UI.P2_moc_suwak.setEnabled(False)
            self.UI.R4_moc_suwak.setEnabled(False)
        else:
            self.UI.P2_moc_suwak.setEnabled(True)
            self.UI.R4_moc_suwak.setEnabled(True)


        self.sledzenie_ok=int(s)
    def zmien_automatyczna_temperatura(self,t):
        self.automatyczna_temperatura=t

#