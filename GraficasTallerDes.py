# -*- coding: utf-8 -*-
"""
Created on Sat May 27 09:37:42 2023

@author: Dastyb
"""

import os
import sys
import datetime
from PyQt5 import QtCore, QtGui, Qt, QtWidgets, uic
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import Archivo_plano
n=200
matplotlib.use("Qt5Agg")

now = datetime.datetime.now()
a= np.arange(1.0, 21.0, 0.1)
function_humedad = [(ai**2)/1000 for ai in a]
function_velocidad = [math.cos(2*math.pi*ai) for ai in a]
function_calidad_aire=[random.randint(0,200) for _ in range(n)]
function_proximidad = [math.sin(2*math.pi*ai) for ai in a]
function_ruido = [random.randint(53,92) for _ in range(n)]

#lectura sensores...

with open("./datos.txt", "w") as file:
    for i in range(len(a)):
        file.write(str(now) + " " + str(round(a[i],5)) + " " +
                   str(round(function_humedad[i],5)) + " " + 
                   str(round(function_velocidad[i],5)) + " " +
                   str(round(function_calidad_aire[i],5)) + " " +
                   str(round(function_proximidad[i],5)) + " " + 
                   str(round(function_ruido[i],5)) + "\n")


class GraficasTallerDes(QtWidgets.QMainWindow):
    def __init__(self):
        super (GraficasTallerDes, self).__init__()
        uic.loadUi("GraficasTaller.ui",self)
        
        self.Grafica_1.clicked.connect(self.a)
        self.Grafica_2.clicked.connect(self.b)
        self.Grafica_3.clicked.connect(self.c)
        self.Grafica_4.clicked.connect(self.d)
        self.Grafica_5.clicked.connect(self.e)
        self.LED.clicked.connect(self.f)
        self.load_data()
    
    def load_data(self):
    
       data = []
       with open("./datos.txt", "r") as file:
           for line in file:
               line_data = line.strip().split()
               data.append(line_data)


       self.tableWidget.setColumnCount(len(data[0]))
       self.tableWidget.setRowCount(len(data))
       self.tableWidget.setHorizontalHeaderLabels(["Fecha", "Hora" ,"Tiempo (s)",
                                                   "Humedad Relativa (%)", "Velocidad (Km/h)",
                                                   "Calidad del aire (ICA)",
                                                   "Proximidad (m)", "Ruido (dB)"])


       for i, row in enumerate(data):
           for j, item in enumerate(row):
               self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(item))
    
    def a(self):
            plt.plot(function_humedad, "-.g", marker= "o")
            plt.title(f"Humedad del ambiente")
            plt.ylabel("Humedad relativa (%)")
            plt.xlabel("Tiempo (s)")
            plt.show()
    
    def b(self):
            plt.plot(function_velocidad, "--c",marker= "p")
            plt.title(f"Velocidad del vehiculo")
            plt.ylabel("Velocidad (Km/h)")
            plt.xlabel("Tiempo (s)")
            plt.show()
    def c(self):
            plt.plot(function_calidad_aire, "-.m",marker= "v")
            plt.title(f"Calidad de aire del ambiente")
            plt.ylabel("Calidad del aire (ICA)")
            plt.xlabel("Tiempo (s)")
            plt.show()        
   
    def d(self):
            plt.plot(function_proximidad, "-b",marker= "*")
            plt.title(f"Distancia del vehiculo")
            plt.ylabel("Distancia(m)")
            plt.xlabel("Tiempo (s)")
            plt.show()
   
    def e(self):
            plt.plot(function_ruido, "--r",marker= "o")
            plt.title(f"Nivel de ruido del vehiculo")
            plt.ylabel("Decibelios(dB)")
            plt.xlabel("Tiempo (s)")
            plt.show()   
    def f(self):
            self.SALIDA_LED.setText(str("OPRIMA EL BOTON PARA PRENDER EL LED"))
            # Pin assignments
            print('Entra a funcion')
            import  RPi.GPIO as GPIO
            LED_PIN = 7
            BUTTON_PIN = 17
            # Setup GPIO module and pins
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LED_PIN, GPIO.OUT)
            GPIO.setup(BUTTON_PIN, GPIO.IN)
            # Set LED pin to OFF (no voltage)
            GPIO.output(LED_PIN, GPIO.LOW)
            print('Ejecutando..')
            try:
                # Loop forever
                while 1:
                    # Detect voltage on button pin
                    if GPIO.input(BUTTON_PIN) == 1:
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        self.SALIDA_LED.setText(str("LED ENCENDIDO"))
                    else:
                        GPIO.output(LED_PIN,GPIO.LOW)
                        self.SALIDA_LED.setText(str("LED APAGADO"))
            except KeyboardInterrupt:
                print('Hecho')
            finally:
                GPIO.cleanup()
            #self.SALIDA_LED.setPixmap(QtGui.QPixmap('./imagenes_redes/5.jpg'))   
            

def main():
    import sys
    print("Inicia programa: Redes Inalámbricas de Sensores Multimedia para el control de tráfico vehicular")
    app=QtWidgets.QApplication(sys.argv)
    ventana=GraficasTallerDes()
    ventana.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
    
