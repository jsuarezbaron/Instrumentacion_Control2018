# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:30:33 2018

@author: Publico
"""

import numpy as np
import nidaqmx as daq
import math
import pylab as plt 
import time

from nidaqmx.constants import LineGrouping
from nidaqmx.types import CtrTime

from nidaqmx import system
s = system.System()
print(list(s.devices)) # data dev correspondiente








#%% 
fs = 1
samples = 1
setpoint =40
kp=0.05
periodoPWM = 0.1
plt.ion()   #habilita modo interactivo de matplotlib

listTemp = []
C_ =[]
ten_ = []
tap_ = []
#--------------------------Medir voltaje analógico-------------------------------
'''
Funciòn que devuelve el voltaje medido en un canal, por ejemplo de un sensor anlaògico
'''
#def medir_volt_anal():
    
def ferror(Temp2,setpoint,kp):
    deltatemp = setpoint - Temp2
    c = kp*deltatemp
    if c>0.99:
            c=0.99
    elif c<-0.99:
            c=-0.99
    return c
        

def contador():

     i=0
     with daq.Task() as task:
         task.co_channels.add_co_pulse_chan_time("Dev3/ctr0",name_to_assign_to_channel = "pwmOut",
                                                 high_time=periodoPWM/2, low_time=periodoPWM/2)
         task.timing.cfg_implicit_timing(sample_mode=daq.constants.AcquisitionType.CONTINUOUS, samps_per_chan=700)
         task.start()
         temperatura=medir_tem()
         while(True):
             temperatura=0.8*temperatura+0.2*medir_tem()
             '''
             guardar temp
             '''
             listTemp.append(temperatura)
             
            #plt.scatter(i,data[1],c='b')
            
             print("Temperatura:", temperatura)
             np.savetxt('Temperatura_prue_final.txt', listTemp, delimiter=' ')
                                     
             i +=1
                          
             c = ferror(temperatura,setpoint,kp)
             tiempo_encendido=periodoPWM*(1-c)/2
             tiempo_apagado=periodoPWM*(1+c)/2
             sampleH = daq.types.CtrTime(high_time=tiempo_encendido, low_time=tiempo_apagado)
             C_.append(c)
             ten_.append(tiempo_encendido)
             tap_.append(tiempo_apagado)
             np.savetxt('C_1.txt', C_, delimiter=' ')
             np.savetxt('ten_1.txt', ten_, delimiter=' ')
             np.savetxt('tap_1.txt', tap_, delimiter=' ')
             
             plt.subplot(212)
             plt.scatter(i,temperatura,c='r', label= 'temperatura')
             plt.subplot(221)
             plt.scatter(i,c,c='b', label= 'c')
             plt.subplot(222)
             plt.scatter(i,tiempo_encendido,c='g', label='tiempo_encendido')
             plt.scatter(i,tiempo_apagado,c='y', label='tiempo_apagado')
             
             plt.pause(0.05)
             print('c=', c)
             print('tiempo_encendido=',tiempo_encendido)
             print('tiempo_apagado=',tiempo_apagado)
             if i%10==0:
                 task.write(sampleH)
             time.sleep(0.15*periodoPWM)
         
         task.wait_until_done
         task.stop()



def activa_salida_digital(activa_o_desactiva):
    #nidaqmx._task_modules.channels.channel.Channel 
    #nidaqmx.system._collections.PhysicalChannelCollection
    with daq.Task() as task:
        #daq.constants.ChannelType(10153)
        task.do_channels.add_do_chan(
            "Dev3/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
        #samples = [True] 
        task.write(activa_o_desactiva)    


def medir_tem():

    with daq.Task() as task:
        ai0 = task.ai_channels.add_ai_voltage_chan("Dev3/ai0",terminal_config = daq.constants.TerminalConfiguration(10083))
        ai0.ai_gain=1
        ai1 = task.ai_channels.add_ai_voltage_chan("Dev3/ai1",terminal_config = daq.constants.TerminalConfiguration(10083))
        ai1.ai_gain=1
        #task.start()
        task.timing.cfg_samp_clk_timing(fs) # seteo la frecuencia de muestreo
        
       
        data = task.read(number_of_samples_per_channel=samples)
        #print(data)
        #plt.plot(np.arange(samples)/fs, data[0], label = 'Canal 0')
        #plt.plot(np.arange(samples)/fs, data[1], label = 'Canal 1')
        Temp = np.asarray(data[0])
        Temp2 = Temp * 100

    return Temp2
'''        
        c = ferror(Temp2,setpoint,kp)
        if c>0.99:
            c=0.99
        elif c<-0.99:
            c=-0.99
        
        tiempo_encendido=tiempo_total*(1-c)
        activa = activa_salida_digital(activa_o_desactiva=False)
        time.sleep(tiempo_encendido)
        tiempo_apagado=tiempo_total*(1+c)
        desactiva = activa_salida_digital(activa_o_desactiva=True)
        time.sleep(tiempo_apagado)
        #print(data)
        #if Temp2<50:
            #activa = activa_salida_digital(activa_o_desactiva=False)
        #if Temp2>55:
            #desactiva = activa_salida_digital(activa_o_desactiva=True)
'''


