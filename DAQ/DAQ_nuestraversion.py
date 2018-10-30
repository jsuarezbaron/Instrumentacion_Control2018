#se crea digital, se emite analogico, se mide analogico y el DAQ lo digitaliza

import pylab as plt 
import time as t
import numpy as np		
import nidaqmx
import pprint
#probamos un diagnostico para ver si reconoce la placa DAQ y que nombre le está dando
#------------         Diagnostico      ------------
#correr esto primero  y ver que nombre le pone al device!!

fSampling = 1000 #Hz
nSamples = 1024 #samples
#pp = pprint.PrettyPrinter(indent=4)
dtMax = 2 #sec



from nidaqmx import system
s = system.System()
print(list(s.devices)) 


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev10/ai1")
    print(task.read())
'''
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev10/ai1")
    data0 = task.read(number_of_samples_per_channel=1000)
    #print(data)
    plt.plot(data0, label = 'Canal 0')
    #plt.xlimi([])
    plt.legend(loc='upper right')
    plt.show()
'''

with nidaqmx.Task() as task:
    t1 = t.time()
    task.ai_channels.add_ai_voltage_chan("Dev10/ai1")
    #data1 = task.read(number_of_samples_per_channel=1024)
    data1 = task.read(number_of_samples_per_channel=nSamples)
    #print(data)
    task.timing.cfg_samp_clk_timing(fSampling)
    t2 = t.time()
    dt = t2 - t1
    while dt < dtMax:
        data = task.read(number_of_samples_per_channel=nSamples)
        t2 = t.time()
        dt = t2-t1
        print (dt)
        pp.pprint(data)		
    plt.subplot(2,1,1)
    plt.plot(data1, label = 'Canal 1')
    plt.legend(loc='upper right')
    plt.subplot(2,1,2)
    plt.plot(data)
    #plt.xlimi([2, 3])
    #plt.show()










'''
#--------------   Código para generar la señal   --------------
import sounddevice as sd 
import numpy as np 
import pylab as plt 
import time 

  

def generador_de_senhal(frecuencia, duracion, amplitud, funcion, fs=192000): 
    """ 
    Genera una seÃ±al de forma seniodal o de rampa, con una dada frecuencia y duracion. 
    """ 
    cantidad_de_periodos = duracion*frecuencia 
    puntos_por_periodo = int(fs/frecuencia) 
    puntos_totales = puntos_por_periodo*cantidad_de_periodos 
              
    tiempo = np.linspace(0, duracion, puntos_totales) 
    if funcion=='sin': 
          data = amplitud*np.sin(2*np.pi*frecuencia*tiempo) 
    elif funcion=='rampa':
        data = amplitud*signal.sawtooth(2*np.pi*frecuencia*tiempo) 
    else:
        print("Input no vÃ¡lido. Introducir sin o rampa")
        data = 0 
    return tiempo, data 


def play_tone(frecuencia, duracion, amplitud=1, fs=192000, wait=True): 
    """ 
    Esta funciÃ³n tiene como output un tono de una cierta duraciÃ³n y frecuencia. 
    """ 
    sd.default.samplerate = fs #frecuencia de muestreo 
       
    tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'sin')    
    sd.play(data) 
       
    if wait: 
        time.sleep(duracion) 
    
    return tiempo , data 



def playrec_tone(frecuencia, duracion, amplitud=0.5, fs=192000): 
      """ 
      Emite un tono y lo graba. 
      """ 
      sd.default.samplerate = fs #frecuencia de muestreo 
      sd.default.channels = 2,2 #por las dos salidas de audio 
       
      tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'sin')       
      
      with nidaqmx.Task() as task:
          task.ai_channels.add_ai_voltage_chan("Dev8/ai1")
          daq = (task.read())
      
      grabacion = sd.playrec(daq, blocking=True) 
       
      return tiempo, data, grabacion 
  
#playrec_tone(1000,3)

'''

    
    
    
