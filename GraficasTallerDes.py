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




matplotlib.use("Qt5Agg")
now = datetime.datetime.now()

n=200
a= np.arange(1.0, 21.0, 0.1)
function_humedad = [(ai**2)/1000 for ai in a]
function_velocidad = [math.cos(2*math.pi*ai) for ai in a]
function_calidad_aire=[random.randint(0,200) for _ in range(n)]
function_proximidad = [math.sin(2*math.pi*ai) for ai in a]
function_ruido = [random.randint(53,92) for _ in range(n)]

#lectura sensores...
a= np.arange(1.0, 21.0, 0.1)
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
        self.SENSOR.clicked.connect(self.g)
        self.API.clicked.connect(self.h)
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
                
    def g(self):
                    
                    
            self.SALIDA_SENSOR.setText(str("LISTO PARA RECIBIR DATOS DEL SENSOR")) 
            # -*- coding: utf-8 -*-
            from digi.xbee.devices import XBeeDevice
            from digi.xbee.io import IOLine, IOMode
        
            #
            # Raspberry Pi Data Aggregator - Beginning Sensor Networks Second Edition
            #
            # For this script. we read data from an XBee remote data mode
            # from a ZigBee Coordinator connected to a Raspberry Pi via a
            # serial interface.
            
            #
            # The data read includes an analog value from DIO3/AD3 and the current voltage value.
            #
            
            # Serial port on Raspberry Pi
            SERIAL_PORT = "/dev/ttyUSB0"  # "/dev/ttyS0"
            # BAUD rate for the XBee module connected to the Raspberry Pi
            BAUD_RATE = 9600
            # The name of the remote node (NI)
            REMOTE_NODE_ID = "SENSOR2"
            # Analog pin we want to monitor/request data
            ANALOG_LINE = IOLine.DIO3_AD3
            # Sampling rate
            SAMPLING_RATE = 15
            # Get an instance of the XBee device class
            device = XBeeDevice(SERIAL_PORT, BAUD_RATE)
            
            # Method to connect to the network and get the remote node by id
            def get_remote_device():
               """Get the remote node from the network 
               Returns:
               """
               # Request the network class and search the network for the remote node
               xbee_network = device.get_network()
               remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
               if remote_device is None:
                  print("ERROR: Remote node id {0} not found.".format(REMOTE_NODE_ID))
                  exit(1)
               remote_device.set_dest_address(device.get_64bit_addr())
               remote_device.set_io_configuration(ANALOG_LINE, IOMode.ADC)
               remote_device.set_io_sampling_rate(SAMPLING_RATE)
                           
            
            def io_sample_callback(sample, remote, time):
               print("Reading from {0} at {1}:".format(REMOTE_NODE_ID, remote.get_64bit_addr()))
               # Get the temperature in Celsius
               #temp_c = ((sample.get_analog_value(ANALOG_LINE) * 1200.0 / 1024.0) - 500.0) / 10.0
               # Calculate temperature in Fahrenheit
               #temp_f = ((temp_c * 9.0) / 5.0) + 32.0
               #print("\tTemperature is {0}C. {1}F".format(temp_c, temp_f))
               # Calculate supply voltage
               humedad = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
               print("\tSupply voltage = {0}v".format(humedad))
               
               #definicion funciones
               velocidad = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
               print("\tSupply voltage = {0}v".format(velocidad))
               calidad_aire = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
               print("\tSupply voltage = {0}v".format(calidad_aire))
               proximidad = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
               print("\tSupply voltage = {0}v".format(proximidad))
               ruido = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
               print("\tSupply voltage = {0}v".format(ruido))
               
               
               
               
               with open('muestras2.txt', 'w') as file:
                   file.write("{0} {1} {2} {3} {4} {5}\n".format(now,humedad,velocidad,calidad_aire,proximidad,ruido))
                
               
            try:
               print("Welcome to example of reading a remote sensor with XBEE PRO S2!")
               device.open() # Open the device class
               # Setup the remote device
               get_remote_device()
               # Register a listener to handle the samples received by the local device.
               device.add_io_sample_received_callback(io_sample_callback)
               while True:
                   pass
            except KeyboardInterrupt:
               if device is not None and device.is_open():
                  device.close()


            #API ------------------------------------------------------------------------------
                    
    def h(self):
            self.SALIDA_API.setText(str("CARGA Y GRAFICA EN THINGSPEAK")) 
            # -*- coding: utf-8 -*-
            
            #from __future__ import print_function
            #import print_function
            # Python imports
            import http.client
            import time
            import urllib
            #valores
            n=200
            a= np.arange(1.0, 21.0, 0.1)
            
            
            # API KEY
            THINGSPEAK_APIKEY = 'M1OVE1I52Q9QYIV2'
            print("Welcome to the ThingSpeak Raspberry Pi temperature sensor! Press CTRL+C to stop.")
            try:
              while 1:
                 # Get temperature in Celsius
                 #hum = ((500 * 3.30) - 0.5) * 10
                 # Calculate temperature in Fahrenheit
                 #vel = (temp_c * 9.0 / 5.0) + 32.0
                 function_humedad = random.randint(10,100)
                 function_velocidad = random.randint(0,60)
                 function_calidad_aire=random.randint(0,200)
                 function_proximidad = random.randint(200,1000)
                 function_ruido = random.randint(53,92) 
                 # Display the results for diagnostics
                 print("Uploading {0:.2f} C, {1:.2f} F" "".format(function_humedad,
                 function_velocidad,function_calidad_aire,function_proximidad,function_ruido), end=' ... ')
                 # Setup the data to send in a JSON (dictionary)
                 params = urllib.parse.urlencode(
                      {
                         'field1': function_humedad,
                         'field2': function_velocidad,
                         'field3': function_calidad_aire,
                         'field4': function_proximidad,
                         'field5':function_ruido,
                         'key': THINGSPEAK_APIKEY,
                      }
                 )
                 # Create the header
                 headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': "text/plain"}
                 # Create a connection over HTTP
                 conn = http.client.HTTPConnection("api.thingspeak.com:80")
                 try:
                     # Execute the post (or update) request to upload the data
                     conn.request("POST", "/update", params, headers)
                     # Check response from server (200 is success)
                     response = conn.getresponse()
                     # Display response (should be 200)
                     print("Response: {0} {1}".format(response.status,response.reason))
                     # Read the data for diagnostics
                     data = response.read()
                     conn.close()
                 except Exception as err:
                     print("WARNING: ThingSpeak connection failed: {0}, " "data: {1}".format(err, data))
                 # Sleep for 20 seconds
                 time.sleep(20)
            except KeyboardInterrupt:
                 print("Thanks, bye!")
            exit(0)
def main():
    import sys
    print("Inicia programa: Redes Inalámbricas de Sensores Multimedia para el control de tráfico vehicular")
    app=QtWidgets.QApplication(sys.argv)
    ventana=GraficasTallerDes()
    ventana.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
    
