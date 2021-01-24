import sounddevice as sd
#Libraries to Utterance Detection
import prefiltration as pref
import acquisition as acq
import hammingWindows as hamm
import treshold as tresh
import output as out
import asyncio

async def periodic():
    while True:
        #____________________Step 0: Initialization____________________
        acq.reiniData()
        acq.data["rate"] = 22050
        acq.data["duration"] = 3
        acq.data["channels"] = 1
        #____________________Step 1: Sound Acquisition____________________
        cr = acq.CommandRecorder() #create object
        acq.data["rec"] = cr.record_sound() #start recording
        sd.play(acq.data["rec"], acq.data["rate"]) #play recorded audio
        #cr.plot22k() #plot recorded audio in frequency equal 22kHz
        cr.convertToLowerFreq() #create 11kHz record based at 22kHz
        acq.data["rate"] = 11025
        #cr.plot11k() #plot recorded audio in frequency equal 11kHz
        #____________________Step 2: Pre-filtration____________________
        pref.FFT(0) #Fast Fourier Transformate to detect frequency of noises; At input 1 means plot FFT
        pref.createFilter(0) #At input 1 means plot Filter
        pref.startFiltering() #Filter speech
        #pref.plotFilteringResults()
        #____________________Step 3: Hamming Window Implementation____________________
        hamm.execute() #Converts 1D voice array to 2D and use Hamming Window function at signal
        #hamm.plot()
        #____________________Step 4: Treshold Detection____________________
        tresh.execute() #
        #tresh.plot()
        #____________________Step 5: Start / End Time____________________
        out.medianFiltering()
        #out.plotMedianFilter()
        out.findIndexes()
        out.estimateTimes()
        #out.plotFilteredUtterance()
        #out.plotUtteranceFrame()
        out.plotOverallUtterance()

        await asyncio.sleep(0)

def stop():
    task.cancel()

loop = asyncio.get_event_loop()
task = loop.create_task(periodic())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass