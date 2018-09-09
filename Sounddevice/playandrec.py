import sounddevice as sd
import numpy as np
from numpy import arange
import pylab as plt
import time
from scipy.signal import find_peaks
from scipy import signal

frecuencia=5000  # frecuencia del tono que se desea emitir
duracion=1       # duracion del tono

def playrec_tone(frecuencia, duracion, amplitud=0.5, fs=200000):
    """
    Emite un tono y lo graba.
    """
    sd.default.samplerate = fs # frecuencia de muestreo
    sd.default.channels = 2,2  # por las dos salidas de audio
    
    cantidad_de_periodos = duracion*frecuencia
    puntos_por_periodo = int(fs/frecuencia)
    puntos_totales = puntos_por_periodo*cantidad_de_periodos

    tiempo = np.linspace(0, duracion, puntos_totales)  # interpola puntos_totales entre 0 y duracion

    data = amplitud*np.sin(2*np.pi*frecuencia*tiempo)  # funcion que genera los datos para el ono
    
    grabacion = sd.playrec(data, blocking=True)        # graba los datos de entrada (line in)

    plt.subplot(2,1,1)                                 
    plt.plot(tiempo, data,'b.--')                      # grafica datos emitidos
    plt.xlim([0.524, 0.525])
    plt.subplot(2,1,2)
    plt.plot(tiempo, grabacion,'r.--')                 # grafica datos grabados (line in o input) 
    plt.xlim([0.524, 0.525])

    
    return tiempo, data, grabacion

datos=playrec_tone(frecuencia,duracion)                # datos contiene los arrays concatenados de tiempo, data, grabacion
tiempo=datos[0]                                       
data=datos[1]
grabacion=datos[2]

with open("resultados_frecuencia=" + str(frecuencia) + ".txt", "w") as out_file:     # abre un archivo .txt, str(imprime el valor de la frecuencia)
    for i in range(len(tiempo)):                                           # tiempo, data y grabacion tienen las mismas dimensiones, un for para leer todo el array
        out_string = ""                                                    # string vacio
        out_string += str(tiempo[i])                                       # escribimos los valores de tiempo,data y grabacion
        out_string += "," + str(data[i])
        out_string += "," + str(grabacion[i])
        out_string += "\n"
        out_file.write(out_string)                                         # escribe el string en el archivo de salida


