import random
from scipy.io.wavfile import read as wav_read, write as wav_write
from scipy import hanning, zeros, real
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as pltclr
import matplotlib.gridspec as gridspec
from scipy.signal import spectrogram, stft, istft
import os 
import traceback as tb

# from autoencoders import autoencode, autoencode_conv


class wav(object):
    
    DEFAULT_SAMPLE_RATE = 44100
    MAX_PLOT_POINTS = 1000

    def __init__(
        self,
        filepath_or_array,
    ):
        if isinstance(filepath_or_array, str):
            self.sample_rate, self.data = wav_read(filepath_or_array)
            self.data = self.data / (2.**15.)
        elif isinstance(filepath_or_array, wav):
            self.sample_rate, self.data = filepath_or_array.sample_rate, filepath_or_array.data
        elif len(filepath_or_array) == 2 and not isinstance(filepath_or_array, np.ndarray):
            self.sample_rate, self.data = filepath_or_array[0], np.asarray(filepath_or_array[1])
        else:
            self.sample_rate, self.data = self.DEFAULT_SAMPLE_RATE, np.asarray(filepath_or_array)
        
        if len(self.data.shape) == 1:
            self.data = self.data.reshape(self.data.size, 1)
        
        self.shape = self.data.shape
        self.size, self.channels = self.shape
        self.length = float(self.size/self.sample_rate)
        self.time = np.arange(0, self.length, 1.0/float(self.sample_rate))

    def __len__(
        self,
    ):
        return self.size

    def fft(
        self,
    ):
        return wav(np.fft.rfft(self.data, axis=0)) 

    def ifft(
        self,
    ):
        return wav(np.fft.irfft(self.data, axis=0))


    def stft(
        self,
        window_size=1000,
    ):
        return stft(self.data.squeeze(), fs=self.sample_rate, nperseg=window_size, padded=True)[2]

    @staticmethod
    def prepare_multiple(
        wavlist,
        window_size=500,
    ):
        if all(map(lambda x: type(x) == str, wavlist)):
            wavlist = [wav(w) for w in wavlist]
        sized = [w.stft(window_size) for w in wavlist]
        stacked = np.hstack([np.vstack([s.real, s.imag]) for s in sized])
        index = [w.shape[1] for w in sized]
        return stacked, index

    @staticmethod
    def reconstruct_multiple(
        stacked,
        index,
        sample_rate=44100
    ):
        index_sum = [0,] + [sum(index[:i + 1]) for i in range(len(index))]
        unstacked = [np.asarray(np.split(stacked[:,index_sum[i]:index_sum[i+1]],2)) for i in range(len(index))]
        return [wav(istft(s[0] + 1j*s[1], fs=sample_rate)[1]) for s in unstacked]

    @staticmethod
    def reconstruct_reps(
        reps,
        index
    ):
        index_sum = [0,] + [sum(index[:i + 1]) for i in range(len(index))]
        return [wav(reps.T[:,index_sum[i]:index_sum[i+1]]) for i in range(len(index))]

    def get_plotinfo(
        self,
        subset=None,
        rate=None,
    ):
        if subset is None:
            subset=(0.,1.)
        
        pcg = subset[1] - subset[0]
        
        subset=[int(elt*self.size) for elt in subset]

        size = subset[1] - subset[0]
        length = (size)/self.sample_rate

        if rate is None:
            n_points = int(self.MAX_PLOT_POINTS)
        else:
            n_points = int((rate/self.sample_rate)*size)

        n_points = min(n_points, size)

        index = np.sort(random.sample(set(np.arange(subset[0], subset[1], 1)), n_points))

        time = self.time[index]
        data = self.data[index]

        return time, data

    def plot(
        self,
        subset=None,
        rate=None
    ):

        time, data = self.get_plotinfo(subset, rate)

        for i in range(self.channels):
            plt.plot(time, data[:,i], label='channel {}'.format(i + 1), alpha=0.5)
        
        plt.legend()
        plt.show() 

        # return self.time[index], self.data[index]

    def get_specinfo(
        self,
        one_sided=True,
        cmap=None,
        plot_log=True,
    ):
        f,t,Sxx = spectrogram(self.data.mean(axis=1), fs=self.sample_rate, return_onesided=one_sided)
        return (t,f if one_sided else np.fft.fftfshift(f), Sxx if one_sided else np.fft.fftshift(Sxx, axes=0)), {'cmap': cmap, 'norm': pltclr.LogNorm() if plot_log else None}

    def spec(
        self,
        one_sided=True,
        cmap=None,
        plot_log=True,
    ):
        args, kwargs = self.get_specinfo(one_sided,cmap,plot_log)

        plt.pcolormesh(
            *args,
            **kwargs,
        )

        plt.title('{}-scaled spectrum plot'.format('log' if plot_log else 'linear'))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.colorbar()
        plt.show()

    @staticmethod
    def plot_multiple(
        wavs,
        wav_names=None,
        n_cols=5,
        *args,
        **kwargs,
    ):

        if isinstance(wavs, dict):
            wav_names = list(wavs.keys())
            wavs = list(wavs.values())

        if len(wavs) < n_cols:
            n_cols = int(np.sqrt(len(wavs)))

        width = n_cols
        length = len(wavs) // n_cols + (1 if len(wavs) % n_cols > 0 else 0)

        fig, axes = plt.subplots(length, width, figsize=(1.5*width,1.5*length))

        gs1 = gridspec.GridSpec(width, length)
        gs1.update(wspace=0., hspace=0.)

        axes = np.asarray(axes).ravel()
        
        argslist = [w.get_plotinfo(*args, **kwargs) for w in wavs]
        for i in range(len(wavs)):

            ax = axes[i]
            time, data = wavs[i].get_plotinfo(*args, **kwargs)
            for i in range(wavs[i].channels):
                ax.plot(time, data[:,i], alpha=0.5)

        for ax in axes:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.axis('off')

        plt.tight_layout()

        if wav_names is not None:
            for i in range(len(wavs)):
                axes[i].set_title(wav_names[i], fontsize=6)

        plt.show()

    @staticmethod
    def spec_multiple(
        wavs,
        wav_names=None,
        n_cols=5,
        *args,
        **kwargs,
    ):

        if isinstance(wavs, dict):
            wav_names = list(wavs.keys())
            wavs = list(wavs.values())

        if len(wavs) < n_cols:
            n_cols = int(np.sqrt(len(wavs)))
        
        width = n_cols
        length = len(wavs) // n_cols + (1 if len(wavs) % n_cols > 0 else 0)

        fig, axes = plt.subplots(length, width, figsize=(1.5*width,1.5*length))

        gs1 = gridspec.GridSpec(width, length)
        gs1.update(wspace=0., hspace=0.)

        axes = np.asarray(axes).ravel()
        
        argslist = [w.get_specinfo(*args, **kwargs) for w in wavs]
        for i in range(len(wavs)):
            ax = axes[i]
            im = ax.pcolormesh(
                *argslist[i][0],
                **argslist[i][1],
            )
            # if wav_names is not None:
            #     ax.set_title(wav_names[i], fontsize=6)

        for ax in axes:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.axis('off')

        plt.tight_layout()

        if wav_names is not None:
            for i in range(len(wavs)):
                axes[i].set_title(wav_names[i], fontsize=6)

        return plt.gca()

    def write(
        self,
        name='temp',
    ):
        wav_write(
            '{}{}'.format(name,'' if '.wav' in name else '.wav'),
            int(self.sample_rate),
            (self.data*(2.**15.)).astype(np.int16),
        )

    def compress(
        self,
        n_samples,
    ):
        n_samples = min(self.size, n_samples)
        print('desampling by a factor of {}'.format(self.size/n_samples))
        index = random.sample(range(self.size), n_samples)
        return wav(self.data[index])

    def autoencode(
        self,
        name=None,
        *args,
        **kwargs,
    ):
        if name is None:
            name = 'wav_autoenc_{}'.format('x'.join(map(str, self.shape)))
        
        # single channel
        data = wav(self.data.mean(axis=1)).data.T
        auto_locals = autoencode(data, name=name, *args, **kwargs)

        pdata = auto_locals['autoencoder'].predict(data)

        wav(np.vstack([np.squeeze(data),np.squeeze(pdata)]).T).plot()

        wav(pdata.T).write('{}_OUT'.format(name))

        return data, pdata, auto_locals

    @staticmethod
    def autoencode_multiple(
        wavs,
        name=None,
        threshold=.9,
        slice_=1000,
        *args,
        **kwargs,
    ):

        # single channel, cleanup
        data = wav.clean_dataset(wavs,threshold=threshold,slice_=slice_)

        wavs = [wav(datum) for datum in data]

        if name is None:
            name = 'wav_autoenc_{}'.format('x'.join(map(str, data.shape)))

        auto_locals = autoencode(data, name=name, *args, **kwargs)

        reps = auto_locals['encoder'].predict(data)

        pdata = auto_locals['decoder'].predict(reps)

        # new_wavs = [wav(np.vstack([np.squeeze(d),np.squeeze(pd)]).T) for d,pd in zip([data,pdata])]
        new_wavs = [wav(elt) for elt in pdata]

        i = random.sample(range(len(wavs)), 1)[0]
        new_wavs[i].write('pred_test')
        wavs[i].write('pred_true')

        comp = [wav(np.asarray([np.vstack([w.data, np.zeros((len(wp) - len(w), 1))]), wp.data]).T.squeeze()) for w,wp in zip(wavs, new_wavs)]

        return (wavs, new_wavs, comp), reps, auto_locals

    @staticmethod
    def clean_dataset(
        wavs,
        threshold=1.,
        slice_=None,
    ):
        if isinstance(wavs, dict):
            wavs = list(wavs.values())

        size = len(wavs)
        if threshold > 1.:
            index = np.where(np.asarray(list(map(len, wavs))) < int(threshold))[0]
        else:
            index = np.argsort(list(map(len,wavs)))[:int(size*threshold)]

        wavs = [w for i,w in enumerate(wavs) if i in index]
        
        
        clean = np.zeros((len(wavs), max(map(len, wavs))))
        for i, elt in enumerate(wavs):
            clean[i, 0:len(elt)] = np.mean(elt.data, axis=1)
        
        if slice_ is not None:
            clean = clean[:,slice_]

        return clean

    def __getitem__(
        self,
        key,
    ):
        return wav(self.data[key])

    def __add__(
        self,
        other,
    ):
        return np.hstack([self.data, other.data])

    def __str__(
        self,
    ):
        return 'wav obj. {} samples, {:.3f} seconds'.format(self.size, self.length)

    def __repr__(
        self,
    ):
        return str(self)
