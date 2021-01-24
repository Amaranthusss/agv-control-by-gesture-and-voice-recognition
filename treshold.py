import numpy as np
import matplotlib.pyplot as plt
import acquisition as acq
#-------------------------------------------
#            Treshold Detection
#-------------------------------------------

def execute():
    #__________While loop__________
    for i in range(len(acq.data["framesMatrix"])):
        acq.data["whileData"].append(0)
        for j, jVal in enumerate(acq.data["framesMatrix"][i]):
            acq.data["whileData"][i] = pow(acq.data["framesMatrix"][i][j],2) + acq.data["whileData"][i]
    #__________Sorting array by ASC__________
    whileToMean = []
    for item in acq.data["whileData"]:
        whileToMean.append(item)
    whileToMean.sort()
    idx = 14
    maxIdx = idx
    if idx > len(whileToMean):
        maxIdx = len(whileToMean)
    firstArray = []
    for i in range(maxIdx):
        firstArray.append(whileToMean[i])
    #__________Estimate mean of firstArray__________
    mean = sum(firstArray) / len(firstArray)
    #__________Boolean frame energy__________
    acq.data["tresholdEnergy"] = mean * 2000
    for i in range(len(acq.data["whileData"])):
        if acq.data["whileData"][i] > acq.data["tresholdEnergy"]:
            acq.data["booleanFrameEnergy"].append(1)
        else:
            acq.data["booleanFrameEnergy"].append(0)
    #__________Finish rest of calculations__________
    acq.data["size"] = len(acq.data["whileData"])
    acq.data["summary"] = sum(acq.data["whileData"])

    #print(acq.data["out"].__dict__)

def plot():
    #__________Energy Graph__________
    x = np.arange(len(acq.data["whileData"]))
    plt.figure()
    plt.plot(x,acq.data["whileData"])
    plt.plot([0, len(acq.data["whileData"])], [acq.data["tresholdEnergy"], acq.data["tresholdEnergy"]], '--', label='Treshold Energy')
    plt.title("Energy Graph")
    plt.ylabel("Amplitude")
    plt.xlabel("Sample")
    plt.legend()
    plt.show()
    #__________Boolean Energy Graph__________
    x = np.arange(len(acq.data["booleanFrameEnergy"]))
    plt.figure()
    plt.plot(x,acq.data["booleanFrameEnergy"])
    plt.title("Boolean Frame Energy")
    plt.ylabel("Amplitude")
    plt.xlabel("Sample")
    plt.show()