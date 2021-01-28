import asyncio

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import acquisition as acq
#-------------------------------------------
#            Sound Acquisition
#-------------------------------------------
data = {
    "rate": 22050,
    "duration": 3,
    "channels": 1,
    "rec": [],
    "rec11k": [],
    "filtered": [],
    "framesMatrix": [],
    "minIndex": 0,
    "maxIndex": 0,
    "smoothEnergy": [],
    "simples": 0,
    "startTime": 0,
    "endTime": 0,
    "length": 0,
    "prefN": 0,
    "currHamming": [],
    "windowedHamming": [],
    "tresholdEnergy": 0,
    "size": 0,
    "summary": 0,
    "booleanFrameEnergy": [],
    "whileData": []
}

class CommandRecorder(object):
    def __init__(self, sampleRate = data["rate"], channels = data["channels"]):
        self.sampleRate = sampleRate
        self.channels = channels

    async def record_sound(self, recDuration = data["duration"]):
        samplesToRecord = int((recDuration) * self.sampleRate)
        print('Recording sound!')
        rec = sd.rec(samplesToRecord, samplerate=self.sampleRate,
                     channels=self.channels)
        #sd.wait()
        await asyncio.sleep(recDuration)
        return rec[:, 0]
        
    async def plot22k(self):
        plt.figure()
        t = np.arange(data["rate"] * data["duration"])
        plt.plot(t, data["rec"])
        plt.title("Input Speech [Sample Rate: 22050]")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")
        plt.show()

    async def plot11k(self):
        plt.figure()
        plt.plot(data["rec11k"])
        plt.title("Input Speech [Sample Rate: 11025]")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")
        plt.show()

    async def convertToLowerFreq(self):
        for i in range(len(data["rec"])):
            if i % 2:
                data["rec11k"].append(data["rec"][i])

async def reiniData():
    acq.data = {
        "rate": 22050,
        "duration": 3,
        "channels": 1,
        "rec": [],
        "rec11k": [],
        "filtered": [],
        "framesMatrix": [],
        "minIndex": 0,
        "maxIndex": 0,
        "smoothEnergy": [],
        "simples": 0,
        "startTime": 0,
        "endTime": 0,
        "length": 0,
        "prefN": 0,
        "currHamming": [],
        "windowedHamming": [],
        "tresholdEnergy": 0,
        "size": 0,
        "summary": 0,
        "booleanFrameEnergy": [],
        "whileData": []
    }