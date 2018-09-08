import sounddevice as sd
import numpy as np
import pylab as plt
import time
from scipy.signal import find_peaks
from scipy import signal



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
    
    return tiempo, data, grabacion


