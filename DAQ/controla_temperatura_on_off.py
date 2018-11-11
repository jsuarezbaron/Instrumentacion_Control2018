# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:52:43 2018

@author: Publico
"""



import numpy as np
import nidaqmx as daq
import math
import pylab as plt 

from nidaqmx.constants import LineGrouping
from nidaqmx.types import CtrTime

from nidaqmx import system
s = system.System()
print(list(s.devices)) # data dev correspondiente




#%% 

#--------------------------Medir voltaje analógico-------------------------------
'''
Funciòn que devuelve el voltaje medido en un canal, por ejemplo de un sensor anlaògico
'''
#def medir_volt_anal():
    
    
def activa_salida_digital(activa_o_desactiva):
    #nidaqmx._task_modules.channels.channel.Channel 
    #nidaqmx.system._collections.PhysicalChannelCollection
    with daq.Task() as task:
        #daq.constants.ChannelType(10153)
        task.do_channels.add_do_chan(
            "Dev10/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
        #samples = [True] 
        task.write(activa_o_desactiva)    
    
fs = 1
samples = 1

plt.ion()   #habilita modo interactivo de matplotlib
i = 0

with daq.Task() as task:
    ai0 = task.ai_channels.add_ai_voltage_chan("Dev10/ai0",terminal_config = daq.constants.TerminalConfiguration(10083))
    ai0.ai_gain=1
    ai1 = task.ai_channels.add_ai_voltage_chan("Dev10/ai1",terminal_config = daq.constants.TerminalConfiguration(10083))
    ai1.ai_gain=1
    #task.start()
    task.timing.cfg_samp_clk_timing(fs) # seteo la frecuencia de muestreo
    
    while (True):
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
        if Temp2<25:
            activa = activa_salida_digital(activa_o_desactiva=True)
        if Temp2>30:
            desactiva = activa_salida_digital(activa_o_desactiva=False)

	with open("temp" + str(delta) + ".txt", "w") as out_file:
            for i in range(len(Temp2)):
                out_string = ""
                #out_string += str(tiempo[i])
                out_string += str(Temp2[i])
                #out_string += "," + str(grabacion[i])
                out_string += "\n"
                out_file.write(out_string)
        return Temp2	

## voy a medir la amplitud máxima para ver que tan 1 es la ganancia 1 y tener esto caracterizado para un sensor.
#from daq._task_modules.channels.channel import Channel
#from daq.constants import (
#    ActiveOrInactiveEdgeSelection, DataTransferActiveTransferMode,
#    DigitalDriveType, Level, LogicFamily, OutputDataTransferCondition)         

###########do_line (Dev8,chn,hsi)

#%%
'''
   
def activa_salida_digital():
    #nidaqmx._task_modules.channels.channel.Channel 
    #nidaqmx.system._collections.PhysicalChannelCollection
    with daq.Task() as task:
        #daq.constants.ChannelType(10153)
        task.do_channels.add_do_chan(
            "Dev10/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
        samples = [True] 
        task.write(samples)
        
#        [[False, True], [True, True]]

'''

       
        
