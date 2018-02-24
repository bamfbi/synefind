import numpy as np
import scipy
from pyAudioAnalysis import audioAnalysis, audioBasicIO
import matplotlib.pyplot as plt

a, b = audioBasicIO.readAudioFile("data/wav2.WAV")
print a
print b
plt.plot(np.arange(0, np.size(b), 1), b)
plt.show()

#[Fs, x] = audioBasicIO.readAudioFile("thunder_strike_3-Mike_Koenig-853886140.wav");
#F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs);
#plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR'); 
#plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy'); plt.show()

