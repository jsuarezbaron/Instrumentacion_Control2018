# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:21:29 2018

@author: usuario
"""

import soundfile as sf

data, samplerate = sf.read('file.wav')
sf.write('new_file.ogg', data, samplerate)