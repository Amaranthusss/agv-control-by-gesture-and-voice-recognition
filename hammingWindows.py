import matplotlib.pyplot as plt
import numpy as np

import acquisition as acq
#-------------------------------------------
#            Hamming Window Implementation
#-------------------------------------------

#This part was required because there's need to change 1D speech array into 2D array
FRAME_SIZE = 0.02 #0.02 means 20 ms frames
dt = 9.07029E-5 #ToDo: not sure why, lets find answer ;) anyway it's constant


def execute():
    frameLength = int(int(FRAME_SIZE / dt) * 0.75)
    forN = int((((len(acq.data["filtered"]) * dt) / FRAME_SIZE * 4) - 1 ) / 3 )
    #Conclusion: forN is doubled because we now use doubled frequency acquisition, it looks fine
    #print (frameLength, forN, int(FRAME_SIZE / dt))

    for i in range(forN):
        acq.data["currHamming"] = [] #to show overall speech remove this and next line of code
        acq.data["windowedHamming"] = []
        currIdx = frameLength * i #should be equal something up to around 32670
        for j in range(currIdx, (currIdx + frameLength)):
            acq.data["currHamming"].append(acq.data["filtered"][j])
        window = np.hamming(len(acq.data["currHamming"])) 
        acq.data["windowedHamming"] = window * acq.data["currHamming"] #1D array
        acq.data["framesMatrix"].append(acq.data["windowedHamming"]) #2D array
    
def plot():
    plt.figure()
    plt.plot(acq.data["currHamming"], label='Last Speech Frame') #this is the last one
    plt.plot(acq.data["windowedHamming"], label='Hamming Windowed') #orange
    plt.title("Implementation of Hamming Window")
    plt.ylabel("Amplitude")
    plt.xlabel("Sample")
    plt.legend()
    plt.show()

#print(framesMatrix)