import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz, butter
from scipy.fft import fft, fftfreq
import numpy as np
import asyncio

import acquisition as acq
#-------------------------------------------
#              Pre-filtration
#-------------------------------------------
LOWCUT = 300.0
HIGHCUT = 800.0


#FFT of input speech
async def FFT(plot):
    acq.data["prefN"] = acq.data["rate"] * acq.data["duration"]
    yf = fft(acq.data["rec11k"])
    xf = fftfreq(acq.data["prefN"], 1 / acq.data["rate"])
    if plot == 1:
        plt.figure()
        plt.title("Filter Coefficients")
        plt.ylabel("Magnitiude")
        plt.xlabel("Frequency")
        plt.plot(xf, np.abs(yf))
        plt.xlim([200, 900])
        plt.show()


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

async def createFilter(plot):
    for order in [3, 6, 9]:
        b, a = butter_bandpass(LOWCUT, HIGHCUT, acq.data["rate"], order=order)
        w, h = freqz(b, a, worN=2000)
        if plot == 1:
            plt.plot((acq.data["rate"] * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
    if plot == 1:
        plt.plot([0, 0.5 * acq.data["rate"]], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.grid(True)
        plt.legend(loc='best')

async def startFiltering():
    acq.data["filtered"] = butter_bandpass_filter(acq.data["rec11k"], LOWCUT, HIGHCUT, acq.data["rate"], order=6)


async def plotFilteringResults():
    t = np.linspace(0, acq.data["duration"], acq.data["prefN"], endpoint=False)
    a = 0.02
    f0 = 300.0
    plt.figure()
    plt.clf()
    plt.plot(t, acq.data["rec11k"], label='Noisy signal')
    plt.plot(t, acq.data["filtered"], label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, acq.data["duration"], linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')
    plt.show()