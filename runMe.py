# Where the main loop of the system will stem from
# This file will spin up instances of other aspects of the system

import time
import json
from RetrieveDataAPI import retrieveData
from ManageSQL import insertData





def main():
    print("Algotrading System initializing...")

    lastTime = time.time()
    targetGap = 15 #seconds

    while True:
        currentTime = time.time()
        timeElapsed = currentTime - lastTime

        if timeElapsed > targetGap:
            #makeAPI call
            apireturn = retrieveData('SHIB_USDT')

            #extract data from gateio.Ticker object using the API getters
            thisLowestAsk = apireturn[0].lowest_ask
            thisHighestBid = apireturn[0].highest_bid
            thisChangePercentage = apireturn[0].change_percentage
            thisVolume = apireturn[0].base_volume

            #store value in our Database
            insertData(time.time(), thisLowestAsk, thisHighestBid, thisVolume, thisChangePercentage)
            
            #reset the time variable
            lastTime = time.time()


if __name__ == "__main__":
    main()


### API response Structure
# [{'base_volume': '1574272009796.8',
#  'change_percentage': '12.08',
#  'currency_pair': 'SHIB_USDT',
#  'etf_leverage': None,
#  'etf_net_value': None,
#  'etf_pre_net_value': None,
#  'etf_pre_timestamp': None,
#  'high_24h': '0.000057937',
#  'highest_bid': '0.000054946',
#  'last': '0.000054955',
#  'low_24h': '0.000048342',
#  'lowest_ask': '0.000054955',
#  'quote_volume': '85260869.242996'}]