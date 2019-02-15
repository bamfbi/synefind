import numpy as np
import scipy as sp 
from pyAudioAnalysis import audioBasicIO
import matplotlib.pyplot as plt

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
