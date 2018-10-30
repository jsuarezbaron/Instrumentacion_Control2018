# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 16:24:13 2018

@author: Publico
"""

import numpy as np
import nidaqmx as daq
import math
import pylab as plt 

from nidaqmx import system
s = system.System()
print(list(s.devices)) # data dev correspondiente




#%% 

#--------------------------Medir voltaje analógico-------------------------------
'''
Funciòn que devuelve el voltaje medido en un canal, por ejemplo de un sensor anlaògico
'''
def medir_volt_anal(modo='diferencial'):
    
    modo_dict = {'diferencial' : 10106,
                 'rse' : 10083}
    
    with daq.Task() as task:
         task.ai_channels.add_ai_voltage_chan("Dev7/ai1") # units = constants.VoltageUnits.VOLTS
         task.ai_channels.add_ai_voltage_chan("Dev7/ai0") #Con el canal1 Ai1 mide bioen el voltaje del LM35
         daq.constants.TerminalConfiguration(modo_dict[modo])
         voltaje=task.read()
         return voltaje
         



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
        task.ai_channels.add_ai_voltage_chan("Dev7/ai0")
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
        
        
       
        
