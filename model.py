# This file will contain models that help us to make decisions on the data incoming from the API
# This is also where the local repository of historical data will be kept

import ManageSQL
import ExitHandler
import numpy as np
import matplotlib.pyplot as plt


def main():
    
    # fetch data from our database and store it in a numpy array
    fetchedData = np.asarray(ManageSQL.fetchPrices())

    # isolate columns of the array
    xvalues = fetchedData[:,4]
    yvalues = fetchedData[:,0]
    

    # plot data 
    plt.plot(xvalues, yvalues)
    plt.show()


    # for x in fetchedData:
    #     print(x[0])
    



main()