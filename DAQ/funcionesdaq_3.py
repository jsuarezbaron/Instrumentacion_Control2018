# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:22:26 2018

@author: Damian
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:52:43 2018

@author: Publico
"""


#import readchar
import numpy as np
import nidaqmx as daq
import math
import time
import pylab as plt 

from nidaqmx.constants import LineGrouping
from nidaqmx.types import CtrTime

from nidaqmx import system
s = system.System()
print(list(s.devices)) # data dev correspondiente




#%% 
#--------------------------Medir voltaje analógico-------------------------------
"""
#Parte para medir temperatura
"""

def medirTemperatura():
    fs = 1

    #valor = 0.1
    #indice =0
    
    with daq.Task() as task:

        ai0 = task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config = daq.constants.TerminalConfiguration(10083))
        ai0.ai_gain=1
        ai1 = task.ai_channels.add_ai_voltage_chan("Dev1/ai1",terminal_config = daq.constants.TerminalConfiguration(10083))
        ai1.ai_gain=1
        #task.start()
        task.timing.cfg_samp_clk_timing(fs) # seteo la frecuencia de muestreo
        
        data = task.read(number_of_samples_per_channel=1)
        #plt.plot(np.arange(samples)/fs, data[0], label = 'Canal 0')
        #plt.plot(np.arange(samples)/fs, data[1], label = 'Canal 1')
        Temp = np.asarray(data[0])
        Temp2 = Temp * 100
        return Temp2

            
def manejarSalidaDigital(): 
    indice = 0
    
    lazo = PIDController(36, 0.1, 2, 0)    #Acà se indican los paràmetros del PID
    #indice = 0
    temperatura = 20.0
    cicloTrabajo = 0.5
    periodo =5.0
    vectorTemp=[]
    vectorInd =[]
    
    with daq.Task() as task2:
        task2.do_channels.add_do_chan("Dev1/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
        # Read a key
        #key = readchar.readchar()
        
        while (True):
            temperatura = medirTemperatura()
            vectorTemp.append(temperatura)
            vectorInd.append(indice)
            plt.scatter(vectorInd,vectorTemp,c='r')
            plt.pause(0.05)
            #plt.scatter(i,data[1],c='b')      
            #print("Temperatura:",temperatura)
            print("Temperatura:",temperatura)
            indice+=1
            #Acà se calculan los tiempos de acuerdo al PID
            #Debe devolver un ciclo de trabajo
            cicloTrabajo = lazo.calculate(temperatura) #Segùn el error del PID
            #cicloTrabajo = temperatura #Segùn el error del PID
            task2.write(True)    
            time.sleep(periodo * cicloTrabajo)
            task2.write(False)
            time.sleep(periodo - periodo * cicloTrabajo)
            
            

class PIDController:

    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.last_error = 0
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0

    def calculate(self, feedback_value):
        error = self.setpoint - feedback_value

        delta_error = error - self.last_error

        self.p_term = self.kp * error
        self.i_term += error
        self.d_term = delta_error

        self.last_error = error
        outValue = self.p_term + (self.ki * self.i_term) + (self.kd * self.d_term)
        if(outValue >1):
            outValue = 1
        elif(outValue < 0):
            outValue = 0 

        return outValue

    
stopCondition = False   #Es para usar esa bander en el while(True) de manejarSalidaDigital()
plt.ion()   #habilita modo interactivo de matplotlib  
manejarSalidaDigital()


        
        
        
    
    
"""
Funciòn para medir el tiempo
"""


## voy a medir la amplitud máxima para ver que tan 1 es la ganancia 1 y tener esto caracterizado para un sensor.
#from daq._task_modules.channels.channel import Channel
#from daq.constants import (
#    ActiveOrInactiveEdgeSelection, DataTransferActiveTransferMode,
#    DigitalDriveType, Level, LogicFamily, OutputDataTransferCondition)         

###########do_line (Dev8,chn,hsi)

#%%

def contador():
     with daq.Task() as task:
         task.co_channels.add_co_pulse_chan_time("Dev1/ctr0")
         sample = CtrTime(high_time=0.01, low_time=0.02)  ## esto esta en segundos
         #task.write(sample)
         task.write(sample)       


#%%
#-------------------------------Medición continua----------------------------

def medir_senal_anal(duracion, fs, chunk=1024, modo='diferencial'):

#modos: rse=10083 ; diferencial=10106

    modo_dict = {'diferencial' : 10106,
                 'rse' : 10083}

    datos = []
    cant_puntos=duracion*fs
    #print(cant_puntos)
    cant_med=math.floor(cant_puntos/chunk)+1
    with daq.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        #task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        task.timing.cfg_samp_clk_timing(fs)
        daq.constants.TerminalConfiguration(modo_dict[modo])
        # print mwchan.physical_channel.ai_term_cfgs (con mwchan=task.ai_channels.add_ai_voltage_chan("Dev1/ai0"))
    
        # while True:
        for i in range(0, cant_med):
            tdata = task.read(number_of_samples_per_channel=chunk)
            datos.extend(tdata)
            plt.plot(datos)
            #print(datos)
            #datos_Med = np.asarray(datos)
            #np.savetxt('datos.txt'.format(datos),datos_Med,delimiter=';')
            
            with open("DatosDAQ=" + str(duracion) + "fs" + str(fs) + ".txt", "w") as out_file:
                for i in range(len(datos)):
                    out_string = ""
                    #out_string += str(tiempo[i])
                    out_string += str(datos[i])
                    #out_string += "," + str(grabacion[i])
                    out_string += "\n"
                    out_file.write(out_string)
        return datos
           
        #np.savetxt('datos{}.txt'.format(datos), delimiter = ';')
        
        
       
        
