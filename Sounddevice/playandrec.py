import sounddevice as sd
import numpy as np
import pylab as plt
import time
from scipy.signal import find_peaks
from scipy import signal

frecuencia=5000
duracion=1

def playrec_tone(frecuencia, duracion, amplitud=0.5, fs=200000):
    """
    Emite un tono y lo graba.
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    sd.default.channels = 2,2 #por las dos salidas de audio
    
    cantidad_de_periodos = duracion*frecuencia
    puntos_por_periodo = int(fs/frecuencia)
    puntos_totales = puntos_por_periodo*cantidad_de_periodos

    tiempo = np.linspace(0, duracion, puntos_totales)

    data = amplitud*np.sin(2*np.pi*frecuencia*tiempo)
    
    grabacion = sd.playrec(data, blocking=True)

    plt.subplot(2,1,1)
    plt.plot(tiempo, data,'b.--')
    plt.xlim([0.524, 0.525])
    plt.subplot(2,1,2)
    plt.plot(tiempo, grabacion,'r.--')
    plt.xlim([0.524, 0.525])

    
    return tiempo, data, grabacion


