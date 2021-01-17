#2D array - [][]
windowedFrames =  [
    [5, 2, 4, 7, 2, 2],
    [8, 5, 4, 7, 8, 4],
    [6, 4, 8, 5, 1, 5],
    [9, 5, 3, 4, 4, 1],
    [6, 4, 2, 4, 4, 1],
] #Simulated data

#__________Initialization output data__________
class Out:
    tresholdEnergy = 0
    size = 0
    summary = 0
    booleanFrameEnergy = 0
out = Out()

#__________While loop__________
whileData = []
for i in range(len(windowedFrames)):
    whileData.append(0)
    for j, jVal in enumerate(windowedFrames[i]):
        whileData[i] = pow(windowedFrames[i][j],2) + whileData[i]
print(whileData)

#__________Sorting array by ASC__________
whileData.sort()
idx = 14
maxIdx = idx
if idx > len(whileData):
    maxIdx = len(whileData)
firstArray = []
for i in range(maxIdx):
    firstArray.append(whileData[i])
#__________Estimate mean of firstArray__________
mean = sum(firstArray) / len(firstArray)
#__________Boolean frame energy__________
out.tresholdEnergy = mean * 10
for i in range(len(whileData)):
    if whileData[i] > out.tresholdEnergy:
        out.booleanFrameEnergy = 1
        #This is true but there was required convert to int
#__________Finish rest of calculations__________
out.size = len(whileData)
out.summary = sum(whileData)

print(out.__dict__)

#O. Szkurlat based at R. Mnair