import numpy as np
import scipy as sp 
from pyAudioAnalysis import audioAnalysis, audioBasicIO
import matplotlib.pyplot as plt

def sinewave(frequency, amplitude, sampleRate=44100, path="data/outfile.wav", length=1):
    sine = np.zeros(length*sampleRate)
    for i in range(np.size(sine)):
        sine[i] = amplitude*np.sin(frequency*2*np.pi*(i/sampleRate))
    sp.io.wavfile.write(path, sampleRate, sine)

sinewave(440, )
        

a, b = audioBasicIO.readAudioFile("data/wav3.WAV")
print "sample rate: ", a
b = np.mean(b, axis=1)

plt.plot(range(np.size(b)), b)
help(ps)
plt.show()

#[Fs, x] = audioBasicIO.readAudioFile("thunder_strike_3-Mike_Koenig-853886140.wav");
#F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs);
#plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR'); 
#plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy'); plt.show()

