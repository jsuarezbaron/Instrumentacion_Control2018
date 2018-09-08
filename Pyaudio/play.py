import sounddevice as sd
import numpy as np
import pylab as plt
import time
from scipy.signal import find_peaks
from scipy import signal

def generador_de_senhal(frecuencia, duracion, amplitud, funcion, fs=192000):
    """
    Genera una señal de forma seniodal o de rampa, con una dada frecuencia y duracion.
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
        print("Input no válido. Introducir sin o rampa")
        data = 0
    return tiempo, data
 
def play_tone(frecuencia, duracion, amplitud=1, fs=192000, wait=True):
    """
    Esta función tiene como output un tono de una cierta duración y frecuencia.
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    
    tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'sin')   
    sd.play(data)
    
    if wait:
        time.sleep(duracion)
        
    return data

def test_play_tone():
    """
    Test para ver si funciona play_tone, tocando varios tonos.
    """
    tones = np.array([165, 175, 196, 220, 247, 262, 294, 330])
    for i in tones:
        play_tone(i, 1)
        time.sleep(1)
        print(i)

def playrec_tone(frecuencia, duracion, amplitud=0.1, fs=192000):
    """
    Emite un tono y lo graba.
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    sd.default.channels = 2,2 #por las dos salidas de audio
    
    tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'sin')      
    grabacion = sd.playrec(data, blocking=True)
    
    return tiempo, data, grabacion

def test_playrec_tone():
    """
    Test para ver si funciona playrec_tone, emitiendo y grabando varios tonos.
    """
    tones = np.array([165, 175, 196, 220, 247, 262, 294, 330])
    for i in tones:
        tiempo, data, grabacion = playrec_tone(i, 1)
        time.sleep(1)
        print(i)
    return grabacion

def record(duracion, fs=192000):
    """
    Graba la entrada de microfono por el tiempo especificado
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    sd.default.channels = 2 #1 porque la entrada es una sola
    
    grabacion = sd.rec(frames = fs*duracion, blocking = True)
    return grabacion

def playrec_delay(freq = 220, tiempo = 3,fs=192000):
    """
    mide el tiempo entre la salida y la entrada de playrec_tone
    con salto distinto de 1 se puede acelerar la medicion pero se sobreestima un poco
    """
    a,b,c = playrec_tone(freq,tiempo)
    det = True
    i = 0
    threshold = np.mean(np.abs(c[20000:-1])) 
    while det:
        if np.abs(c[2000+i]) >= threshold/3:#al principio hay un pico, por eso los 2000
            det = False
        else:
            i = i+1
    return (i+2000)/fs

def frequency_response(points, freqstart = 100, freqend = 10000, duracion = 1):
    """
    Evalua la respuesta en frecuencia del conjunto salida y entrada de audio. Points es que tan denso es el barrido (un numero entero).
    """
    response = np.zeros(points)
    for i in range(points):
        a, d, rec = playrec_tone(freqstart+i/points*(freqend-freqstart),duracion, amplitud = 0.2, fs = 192000)
        response[i] = np.mean(np.abs(rec))
    freq = np.linspace(freqstart, freqend, points)
    plt.figure()
    plt.plot(freq, response, 'b.--')
    plt.xlabel('frecuencia (Hz)')
    plt.ylabel('Respuesta')
    plt.grid()
    return freq, response

def playrec_sawtooth(frecuencia, duracion, amplitud=1, fs=192000):
    """
    Emite y graba una funcion rampa.
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    sd.default.channels = 2,2 #por las dos salidas de audio
    
    tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'rampa')   
    grabacion = sd.playrec(data, blocking=True)
    
    return tiempo, data, grabacion

def barrido_frecuencias_sawtooth():
    """
    Con el circuito armado, repetimos las mediciones para varias frecuencias.
    """
    frecuencias = np.arange(100,1000,100)
    for f in frecuencias:
        t, d, g = playrec_sawtooth(f, 5)
        np.savetxt('datos_diodo_'+str(f)+'hz.txt', np.c_[t, d, -g[:,0], -g[:,1]])
    
#%%
def find_index_of_nearest(array, value):
    """
    Funcion auxiliar que encuentra el indice del elemento mas cercano a cierto valor en un array
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def primera_amplitud_maxima_output(frecuencia, duracion, amplitud):
    """
    Emite un tono y busca el primer maximo a la salida despues del tiempo de delay.
    """
    delay = playrec_delay(frecuencia, tiempo = 3,fs=44100) #el delay se podria calcular una sola vez, no cada vez
    tiempo, data, grabacion  = playrec_tone(frecuencia, duracion, amplitud, fs=44100)
    grabacion = np.concatenate(grabacion, axis=0 ) #la grabacion es una array de arrays y para  buscar picos debe ser uno solo
    peaks, _ = find_peaks(grabacion, height=np.max(grabacion)/4) #busca los picos por encima de 1/4     del maximo valor
    indice_tiempo_delay = find_index_of_nearest(tiempo, delay) #busca el indice del tiempo mas  cercano al delay, para empezar a mirar a partir de ahi
    indice_primer_pico = find_index_of_nearest(peaks, indice_tiempo_delay) #busca el primer pico despues   del tiempo de delay
    primer_pico_maximo  = np.max(peaks[indice_primer_pico:indice_primer_pico+10])
    return grabacion[primer_pico_maximo]

def barrido_amplitudes(frecuencia, duracion, amplitudes= np.linspace(0.1,5,10)):
    amplitudes_output = []
    for a in amplitudes:
        amplitudes_output.append(primera_amplitud_maxima_output(frecuencia, duracion, a))
    return amplitudes_output

def constant(amplitud, duracion,  fs=44100):
    """
    La placa de audio no está hecha para emitir una constante.
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    #x = np.sin(np.linspace(amplitud-0.01, amplitud+0.01, fs*duracion))
    #x = amplitud*np.ones(fs*duracion)+10
    tiempo = 5*np.linspace(0, duracion, 220000)
    
    x = .2*np.sin(2*np.pi*220*tiempo) +.5*np.ones(len(tiempo))
    sd.play(x)
