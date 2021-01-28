import sounddevice as sd
#Libraries to Utterance Detection
import prefiltration as pref
import acquisition as acq
import hammingWindows as hamm
import treshold as tresh
import output as out
import asyncio
import numpy as np

import socket
import matplotlib.pyplot as plt

import sys
sys.path.append('../Speech-Command-Recognition/')

#from SoundCommandClf import SoundCommandClf #ToDo: <UNCOMMENT>
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8089)
client.connect(server_address)
cmdToNum = {'stop':1,'go':1,'left':2,'right':3}
lastCmd = None

async def periodic():
    while True:
        #____________________Step 0: Initialization____________________
        await acq.reiniData()
        acq.data["rate"] = 22050
        acq.data["duration"] = 3
        acq.data["channels"] = 1
        #____________________Step 1: Sound Acquisition____________________
        cr = acq.CommandRecorder() #create object
        acq.data["rec"] = await cr.record_sound() #start recording
        #sd.play(acq.data["rec"], acq.data["rate"]) #play recorded audio #this is synchronous function
        #await cr.plot22k() #plot recorded audio in frequency equal 22kHz
        await cr.convertToLowerFreq() #create 11kHz record based at 22kHz
        acq.data["rate"] = 11025
        #await cr.plot11k() #plot recorded audio in frequency equal 11kHz
        #____________________Step 2: Pre-filtration____________________
        await pref.FFT(0) #Fast Fourier Transformate to detect frequency of noises; At input 1 means plot FFT
        await pref.createFilter(0) #At input 1 means plot Filter
        await pref.startFiltering() #Filter speech
        #await pref.plotFilteringResults()
        #____________________Step 3: Hamming Window Implementation____________________
        await hamm.execute() #Converts 1D voice array to 2D and use Hamming Window function at signal
        #await hamm.plot()
        #____________________Step 4: Treshold Detection____________________
        await tresh.execute() #
        #await tresh.plot()
        #____________________Step 5: Start / End Time____________________
        await out.medianFiltering()
        #out.plotMedianFilter()
        await out.findIndexes()
        await out.estimateTimes()
        #await out.plotFilteredUtterance()
        #await out.plotUtteranceFrame()
        #await out.plotOverallUtterance()
        soundFrame, status = await out.getRec()
        global lastCmd
        lastCmd = str(acq.data["startTime"]) + " " + str(acq.data["endTime"]) + " " + str(acq.data["length"])

        
        #if status==0:  #ToDo: <UNCOMMENT>
            #prediction = clf.classify_rec(soundFrame) #ToDo: <UNCOMMENT>
            #pred = prediction[0] #ToDo: <UNCOMMENT>
            # lastCmd = cmdToNum[pred]
            #print(pred) #ToDo: <UNCOMMENT>
        #else: #ToDo: <UNCOMMENT>
            #print('Status NOK: {}'.format(status)) #ToDo: <UNCOMMENT>

        await asyncio.sleep(0)


async def periodic2():
    global lastCmd
    while True:
        if lastCmd is not None:
            client.send(lastCmd.encode())
        await asyncio.sleep(0.01)

async def analizeData():
    if acq.data['status'] == 1: #command has been cut
        
        await asyncio.sleep(2)

if __name__ == '__main__':
    #clf = SoundCommandClf() #ToDo: <UNCOMMENT>
    loop = asyncio.get_event_loop()
    loop2 = asyncio.get_event_loop()
    loop.create_task(periodic())
    loop2.create_task(periodic2())
    loop.run_forever()
    loop2.run_forever()

