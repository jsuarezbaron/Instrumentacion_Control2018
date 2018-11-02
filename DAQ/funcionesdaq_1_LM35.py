# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:44:47 2018

@author: Publico
"""

import numpy as np
import nidaqmx as daq
import math
import pylab as plt 

from nidaqmx.constants import LineGrouping

from nidaqmx import system
s = system.System()
print(list(s.devices)) # data dev correspondiente


#%% 

#--------------------------Medir voltaje analógico-------------------------------
'''
Funciòn que devuelve el voltaje medido en un canal, por ejemplo de un sensor anlaògico
'''
#def medir_volt_anal():    
    
fs = 1
samples = 1

plt.ion()   #habilita modo interactivo de matplotlib
i = 0

with daq.Task() as task:
    ai0 = task.ai_channels.add_ai_voltage_chan("Dev8/ai0",terminal_config = daq.constants.TerminalConfiguration(10083)) #Importante el código 10083
    ai0.ai_gain=1
    ai1 = task.ai_channels.add_ai_voltage_chan("Dev8/ai1",terminal_config = daq.constants.TerminalConfiguration(10083))
    ai1.ai_gain=1
    #task.start()
    task.timing.cfg_samp_clk_timing(fs) # seteo la frecuencia de muestreo
    
    while (i < 2):
        data = task.read(number_of_samples_per_channel=samples)
        #print(data)
        #plt.plot(np.arange(samples)/fs, data[0], label = 'Canal 0')
        #plt.plot(np.arange(samples)/fs, data[1], label = 'Canal 1')
        Temp = np.asarray(data[0])
        Temp2 = Temp * 100
        plt.scatter(i,Temp2,c='r')
        #plt.scatter(i,data[1],c='b')
        
        print("Temperatura:",Temp2)
        
        plt.pause(0.05)
        i +=1
        print(data)

## voy a medir la amplitud máxima para ver que tan 1 es la ganancia 1 y tener esto caracterizado para un sensor.
#from daq._task_modules.channels.channel import Channel
#from daq.constants import (
#    ActiveOrInactiveEdgeSelection, DataTransferActiveTransferMode,
#    DigitalDriveType, Level, LogicFamily, OutputDataTransferCondition)         

###########do_line (Dev8,chn,hsi)

#%%
'''
Función que activa una salida digital de la Sensor DAQ
'''
def activa_salida_digital():
    #nidaqmx._task_modules.channels.channel.Channel 
    #nidaqmx.system._collections.PhysicalChannelCollection
    app= 'Dev8/port0/line0'
    with daq.Task() as task:
        task.do_channels.add_do_chan(
            app,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
     
        '''
        try:
            print('N Lines 1 Sample Boolean Write (Error Expected): ')
            print(task.write([True, False, True, False]))
        
        except daq.DaqError as e:
            print(e)
        
        
        print('1 Channel N Lines 1 Sample Unsigned Integer Write: ')
        print(task.write(8))
    
        print('1 Channel N Lines N Samples Unsigned Integer Write: ')
        print(task.write([1, 2, 4, 8], auto_start=True))
        '''
        
        task.write(True)
        task.sleep(2)
        task.write(False)
        task.sleep(2)
        
        
    
        


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
        task.ai_channels.add_ai_voltage_chan("Dev8/ai0")
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
        
        
       
        
