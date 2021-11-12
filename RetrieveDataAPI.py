# This file will provide the code to extract the data from the Gate.io API

from __future__ import print_function
import gate_api
import keys
from gate_api.exceptions import ApiException, GateApiException


configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4",
    key = keys.myKey,
    secret = keys.myKeySecret
)

api_client = gate_api.ApiClient(configuration)

api_instance = gate_api.SpotApi(api_client)


def retrieveData(currencyPair):
    try:
        api_response = api_instance.list_tickers(currency_pair=currencyPair)
        print(currencyPair)
        print(api_response)
        return api_response
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling DeliveryApi->list_delivery_contracts: %s\n" % e)
        