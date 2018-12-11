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
setpoint =50
kp=0.27
ki=0.0043
kd=7.029
periodoPWM = 6.0
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
        
def PID_(Temp2,setpoint,kp,ki,kd,i_term,last_error):
    error = setpoint - Temp2
    delta_error = error - last_error
    c = kp*error
    i_term = i_term + error
    d_term = delta_error
    last_error = delta_error
    
    if i_term * ki>0.99:
            i_term=0.99 / ki
    elif i_term<-0.99 / ki:
            i_term=-0.99 /ki
    #pi = c + 
    c += (ki * i_term) + (kd * d_term)
    if c>0.99:
            c=0.99
    elif c<-0.99:
            c=-0.99
            
    return c, i_term
    
    
def PIDFun(Temp2, setpoint, kp, ki, kd, last_error, i_term):
    #Temp2 = Feedback
    
    error = setpoint - Temp2

    delta_error = error - last_error

    p_term = kp * error
    i_term += error
    d_term = delta_error

    last_error = delta_error

    return p_term + (ki * i_term) + (kd * d_term), last_error, i_term    
    
    
    
def contador():

     i=0
     with daq.Task() as task:
         task.co_channels.add_co_pulse_chan_time("Dev13/ctr0",name_to_assign_to_channel = "pwmOut",
                                                 high_time=periodoPWM/2, low_time=periodoPWM/2)
         task.timing.cfg_implicit_timing(sample_mode=daq.constants.AcquisitionType.CONTINUOUS, samps_per_chan=700)
         task.start()
         
         temperatura=medir_temp()
         
         inicialtime = time.time()
         finaltime = inicialtime + periodoPWM
         estado_actual = True 
         activa_salida_digital(estado_actual)
         i_term = 0
         last_error = 0
         while(True):
             temperatura=0.8*temperatura+0.2*medir_temp()
             '''
             guardar temp
             '''
             listTemp.append(temperatura)
             
            #plt.scatter(i,data[1],c='b')
            
             print("Temperatura:", temperatura)
             np.savetxt('Temperatura' + 'kp_' + str(kp) + 'ki_' + str(ki) +'kd_' + str(kd) + 'sp_' + str(setpoint) + '.txt', listTemp, delimiter=' ')
                                     
             i +=1
                          
             #c = ferror(temperatura,setpoint,kp)
             c, i_term = PID_(temperatura,setpoint,kp,ki,kd,i_term,last_error)
             tiempo_encendido=periodoPWM*(1-c)/2
             tiempo_apagado=periodoPWM*(1+c)/2
             sampleH = daq.types.CtrTime(high_time=tiempo_encendido, low_time=tiempo_apagado)
             C_.append(c)
             ten_.append(tiempo_encendido)
             tap_.append(tiempo_apagado)
             np.savetxt('C_' + 'kp_' + str(kp) + 'ki_' + str(ki) +'kd_' + str(kd) + 'sp_' + str(setpoint) + '.txt', C_, delimiter=' ')
             np.savetxt('ten_' + 'kp_' + str(kp) + 'ki_' + str(ki) +'kd_' + str(kd) + 'sp_' + str(setpoint) + '.txt', ten_, delimiter=' ')
             np.savetxt('tap_' + 'kp_' + str(kp) + 'ki_' + str(ki) +'kd_' + str(kd) + 'sp_' + str(setpoint) + '.txt', tap_, delimiter=' ')
             
             #plt.title('Setpoint:', setpoint)
             plt.subplot(212)
             
             plt.scatter(i,temperatura,c='r', label= 'temperatura')
             plt.grid(True)
             plt.subplot(221)
             plt.scatter(i,c,c='b', label= 'c')
             plt.grid(True)
             plt.subplot(222)
             plt.scatter(i,tiempo_encendido,c='g', label='tiempo_encendido')
             plt.scatter(i,tiempo_apagado,c='y', label='tiempo_apagado')
             plt.grid(True)
             plt.pause(0.05)
             print('c=', c)
             print('tiempo_encendido=',tiempo_encendido)
             print('tiempo_apagado=',tiempo_apagado)
             if i%10==0:
                 task.write(sampleH)
             time.sleep(0.15*periodoPWM)
             
             if time.time() > finaltime:
                 inicialtime = time.time()
                 finaltime = inicialtime + periodoPWM
                 estado_actual = not estado_actual 
                 activa_salida_digital(estado_actual)
                 
         task.wait_until_done
         task.stop()



def activa_salida_digital(estado):
    #nidaqmx._task_modules.channels.channel.Channel 
    #nidaqmx.system._collections.PhysicalChannelCollection
    with daq.Task() as task:
        #daq.constants.ChannelType(10153)
        task.do_channels.add_do_chan(
            "Dev13/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
        #samples = [True]
        task.write(estado)
            


def medir_temp():

    with daq.Task() as task:
        ai0 = task.ai_channels.add_ai_voltage_chan("Dev13/ai0",terminal_config = daq.constants.TerminalConfiguration(10083))
        ai0.ai_gain=1
        ai1 = task.ai_channels.add_ai_voltage_chan("Dev13/ai1",terminal_config = daq.constants.TerminalConfiguration(10083))
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





