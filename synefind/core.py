import numpy as np
import scipy as sp 
from pyAudioAnalysis import audioBasicIO
import matplotlib.pyplot as plt

# core functions and class wrappers should be defined here, in the future. 
# for now this will just hold old functions that might/might not be useful
# (only worried about structure for now)
# Probably implement this file last. 

def sinewave_write(frequency=440., amplitude=20000., sampleRate=44100, path="data/outfile.wav", length=1):
    sine = np.zeros(length*sampleRate)
    print np.size(sine)
    for i in range(np.size(sine)):
        sine[i] = amplitude*np.sin(frequency*2.*np.pi*(float(i)/float(sampleRate)))
    sp.io.wavfile.write(path, sampleRate, np.int16(sine))
    


sinewave(amplitude = 30000, length = 12)
        
a, b = audioBasicIO.readAudioFile("data/outfile.wav")

#plt.plot(range(np.size(b)), b)
#plt.show()
