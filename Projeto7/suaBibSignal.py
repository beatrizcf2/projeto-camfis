
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from peakutils.plot import plot as pplot



class signalMeu:
    def __init__(self):
        self.init = 0
        self.fs = 44100
        self.time = 3

    #amostra por segundos
    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure(figsize=(10,6))
        plt.plot(x, np.abs(y))
        plt.grid()
        plt.title('Fourier audio')

    def read_wav(self, filepath):
        data, fs = sf.read(filepath, dtype='float32')  
        return data,fs

    def plot_fourier_peaks(self,x,y,index):
        plt.figure(figsize=(10,6))
        pplot(x, y, index)
        for idx in index:
            plt.annotate(f"{x[idx]:.2f}[Hz]", (x[idx], y[idx]))
        plt.title('Fourier Transform - peaks')
        plt.show()

