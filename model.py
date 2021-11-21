# This file will contain models that help us to make decisions on the data incoming from the API
# This is also where the local repository of historical data will be kept

import ManageSQL
import ExitHandler
import time
import numpy as np
import matplotlib.pyplot as plt

def calcStartTime(interval):
    currentTime = time.time()
    intervalSeconds = 60 * interval
    startTime = currentTime - intervalSeconds
    return startTime

# takes a time interval in minutes
def getData(timeInterval):
    # fetch all data from our database and store it in a numpy array
    # fetchedData = np.asarray(ManageSQL.fetchPrices())
    startTime = calcStartTime(60 * timeInterval)
    endTime = time.time()

    fetchedData = np.asarray(ManageSQL.fetchPrices(startTime, endTime))
    

    # isolate columns of the array
    xvalues = fetchedData[:,4]
    yvalues = fetchedData[:,0]
    
    return [xvalues, yvalues]

    


# calcs the ExponentialMoving average via the CP convolve functionn
# priceData - asset prices, USD
# timieData - associated timestamp
# smoothingFactor - integer inclusively one 1 and 32
def calcEMA(priceData, timeData, smoothingFactor):
    timeDataMod = timeData[smoothingFactor - 2:len(timeData)-1]
    smoothedData = np.convolve(priceData, np.ones(smoothingFactor), 'valid') / smoothingFactor
    return [smoothedData, timeDataMod]


# designed to take the longer array first and shorten it to the length of the short array
def resizeArray(arrays):
    array1 = arrays[0]
    array2 = arrays[1]
    if (len(array1) == len(array2)):
        return array1
    elif(len(array1) > len(array2)):
        difference = len(array1) - len(array2)
        newArray1 = array1[difference: len(array1) - 1]
        return newArray1
    else:
        difference = len(array2) - len(array1)
        newArray2 = array2[difference, len(array2) - 1]
        return array1


def runEMAModel(cashValue, roughSet, smoothSet, timeSet):
    # the current state of the system
    # False if EMA is below the current value
    # True if EMA is above the current value
    state = False
    transitions = []
    localmin = roughSet[0]
    localmax = roughSet[0]


    cashValue = 250


    for i in range(len(timeSet)):

        previousState = state
        # checked to see if the smoothed values have crossed the as traded values
        if (smoothSet[i] <= roughSet[i]):
            state = False
        else:
            state = True
        # record localmin when the states flip
        if(previousState != state and previousState == False):
            localmin = roughSet[i]
        # When a localmax happens record it and simulate the trade
        if(previousState != state and previousState == True):
            
            localmax = roughSet[i]
            
            difference = localmax - localmin
            percentGain = difference / localmin * 100
            cashValue = cashValue * (1 + (percentGain - 0.4) / 100)

            print(cashValue)
            # check to see if we breached the 0.4% trade fee
            if(percentGain > 0.4):
                profitable = True
            else:
                profitable = False

            #record teh transaction
            transitions.append([difference, percentGain, profitable])
    
    return [transitions, cashValue]


def main():
    freshData = getData(60)
    smoothedData = calcEMA(freshData[1], freshData[0], 25)
    print(smoothedData[0])
    roughData = calcEMA(freshData[1], freshData[0], 12)
    print(roughData[0])
    roughDataShortened = resizeArray([roughData[0], smoothedData[0]])
    print(roughDataShortened)
    shortenedTime = resizeArray([freshData[1], smoothedData[0]])
    print(shortenedTime)

    params = runEMAModel(250, smoothedData[0], roughDataShortened, shortenedTime)

    print(params[0])
    print(params[1])





main()