import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt
import pdb
import asyncio

import sys
sys.path.append('../Speech-Command-Recognition/')
#from preprocessing import add_padding_to_sound #ToDo: <UNCOMMENT>

import treshold as tresh
import acquisition as acq
#-------------------------------------------
#            Start / End Time
#-------------------------------------------

async def medianFiltering():
    acq.data["smoothEnergy"] = medfilt(acq.data["booleanFrameEnergy"],3)
    acq.data["simples"] = np.arange(len(acq.data["booleanFrameEnergy"]))

async def plotMedianFilter():
    #plt.plot(x,out.booleanFrameEnergy)
    plt.plot(acq.data["simples"], acq.data["smoothEnergy"])
    plt.title("Boolean Frame Energy & Filtered by Median Filter")
    plt.ylabel("Amplitude")
    plt.xlabel("Sample")
    plt.show()

async def findIndexes():
    negativeEdges = []
    positiveEdges = []
    silent = False
    for i, item in enumerate(acq.data["smoothEnergy"]):
        if (item != acq.data["smoothEnergy"][i - 1]):
            if (item == 1): #Positive Edge
                positiveEdges.append(i)
                silent = True
            elif (item == 0):
                negativeEdges.append(i)
    #Select highest and lowest point to get min and max index
    if silent == True:
        acq.data["minIndex"] = min(positiveEdges)
        acq.data["maxIndex"] = max(negativeEdges)
    #print(acq.data["minIndex"], acq.data["maxIndex"])

async def estimateTimes():
    #Recalculate to time domain
    acq.data["endTime"] = ((acq.data["maxIndex"] * 3 + 1) / 4 ) * 0.02
    acq.data["startTime"] = ((acq.data["minIndex"] * 3 + 1) / 4 ) * 0.02
    acq.data["length"] = acq.data["endTime"] - acq.data["startTime"]
    print(acq.data["startTime"], acq.data["endTime"], acq.data["length"])
    acq.data['status'] = 0
    if acq.data["startTime"] > acq.data["endTime"]: #It means command has been cut
        acq.data['status'] = 1
        print("Command has been cut! Let's try again.")
    elif acq.data["startTime"] == acq.data["endTime"]: #Energy of speech was too low
        acq.data['status'] = 2
        print("There is not any command. Expectancy...")


async def plotFilteredUtterance():
    t = np.arange(acq.data["duration"] * acq.data["rate"])
    plt.figure()
    plt.plot(t/acq.data["rate"], acq.data["filtered"])
    plt.plot([acq.data["startTime"] + acq.data["length"] / 2, acq.data["startTime"] + acq.data["length"] / 2], [min(acq.data["filtered"]), max(acq.data["filtered"])], '--', label= round(acq.data["startTime"] + acq.data["length"] / 2, 2))
    plt.legend(loc='upper left')
    plt.title("Detected Utterance 11k (Filtered)")
    plt.ylabel("Amplitude")
    plt.xlabel("Time [s]")
    plt.xlim([acq.data["startTime"], acq.data["endTime"]])
    plt.show()

async def getRec():
    # pdb.set_trace()
    xStart = int(np.ceil((acq.data["startTime"] + acq.data["length"] / 2 - 0.5)*22050))
    xEnd = int(np.ceil((acq.data["startTime"] + acq.data["length"] / 2 + 0.5)*22050))
    commandFrame = acq.data['rec'][xStart:xEnd]
    if len(commandFrame) < 22050:
        #commandFrame = add_padding_to_sound(commandFrame) #ToDo: <UNCOMMENT>
        print('added padding')
    return commandFrame, acq.data['status']


async def plotUtteranceFrame():
    t = np.arange(acq.data["duration"] * 22050)
    plt.figure()
    plt.plot(t / 22050, acq.data["rec"])
    plt.title("Utterance 22k (Noisy) - 1 Second Frame")
    plt.ylabel("Amplitude")
    plt.xlabel("Time [s]")
    plt.xlim([acq.data["startTime"] + acq.data["length"] / 2 - 0.5, acq.data["startTime"] + acq.data["length"] / 2 + 0.5]) #result rescaled to 1 second frame
    plt.show()


async def plotOverallUtterance():
    t = np.arange(acq.data["duration"] * 22050)
    plt.figure()
    plt.plot(t / 22050, acq.data["rec"])
    plt.plot([acq.data["startTime"], acq.data["startTime"]], [min(acq.data["rec"]), max(acq.data["rec"])], '--', label= round(acq.data["startTime"], 2))
    plt.plot([acq.data["endTime"], acq.data["endTime"]], [min(acq.data["rec"]), max(acq.data["rec"])], '--', label= round(acq.data["endTime"], 2))
    plt.title("Utterance 22k (Noisy) - Overall")
    plt.ylabel("Amplitude")
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()

