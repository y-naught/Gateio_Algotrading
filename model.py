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

def getData():
    # fetch all data from our database and store it in a numpy array
    # fetchedData = np.asarray(ManageSQL.fetchPrices())
    startTime = calcStartTime(60*48)
    endTime = time.time()

    fetchedData = np.asarray(ManageSQL.fetchPrices(startTime, endTime))
    
    #print(fetchedData)

    # isolate columns of the array
    xvalues = fetchedData[:,4]
    yvalues = fetchedData[:,0]
    
    smoothingFactor = 8
    smoothingFactor2 = 12
    smoothingFactor3 = 12

    xvaluesMod = xvalues[smoothingFactor - 2:len(xvalues)-1]
    xvaluesMod2 = xvalues[smoothingFactor2 - 2:len(xvalues)-1]
    xvaluesMod3 = xvalues[smoothingFactor3 - 2:len(xvalues)-1]
    
    smoothed = np.convolve(yvalues, np.ones(smoothingFactor), 'valid') / smoothingFactor
    smoothed2 = np.convolve(yvalues, np.ones(smoothingFactor2), 'valid') / smoothingFactor2
    smoothed3 = np.convolve(yvalues, np.ones(smoothingFactor3), 'valid') / smoothingFactor3

    # the current state of the system
    # False if EMA is below the current value
    # True if EMA is above the current value
    state = False
    transitions = []
    localmin = xvaluesMod3[0]
    localmax = xvaluesMod3[0]

    minTimeBetweenTrades = 5 * 60
    lastTradeTime = xvalues[-1]

    cashValue = 250


    for i in range(len(xvaluesMod3)):

        previousState = state
        # checked to see if the smoothed values have crossed the as traded values
        if (smoothed3[i] <= yvalues[i]):
            state = False
        else:
            state = True
        # record localmin when the states flip
        if(previousState != state and previousState == False):
            localmin = yvalues[i]
        # When a localmax happens record it and simulate the trade
        if(previousState != state and previousState == True):
            
            localmax = yvalues[i]
            
            # adding a time delay between possible trades
            if(lastTradeTime + minTimeBetweenTrades >= xvalues[i]):
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
    
    # print(transitions)
    print(cashValue)

    # plot data 
    plt.plot(xvalues, yvalues)
    plt.plot(xvaluesMod, smoothed)
    plt.plot(xvaluesMod2, smoothed2)
    plt.plot(xvaluesMod3, smoothed3)
    plt.show()

def main():

    # lastTime = time.time()
    # targetGap = 5 # seconds
        
    # currentTime = time.time()
    # timeElapsed = currentTime - lastTime
    
   
    getData()

    # time.sleep(5)

    # for x in fetchedData:
    # print(x[0])
    

#interval is in minutes


main()