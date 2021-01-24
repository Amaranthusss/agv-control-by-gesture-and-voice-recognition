#_________________Get preprocessed sound data from LabView_________________
#This part is only for simulation input data to confirm correct operation of code
#data should be filtered and converted to 2D array with use of Hamming Window function
#datafile = open('windowedFrames.csv', 'r')
#datareader = csv.reader(datafile, delimiter=',')
#csvData = []
#for row in datareader:
#    csvData.append(row) #Filling array with str types
#for i in range(len(csvData)):
#    for j, jVal in enumerate(csvData[i]):
#        csvData[i][j] = float(jVal) #Converting to float
#print(type(csvData[0][0]))
#print(csvData[0][0])
#print(csvData[198][198]) #2D array - [][]