# This file will connect to the database where we will store data we extract from the Gate.io exchange
# This will allow us to make calls to a database without the restrictions of an API to reference historical data, etc

import mysql.connector
import keys


#Add the credentials to your database here
mydb = mysql.connector.connect(
    user = "DATABASE_USERNAME",
    password = "USER_PASSWORD",
    host = "IP_ADDRESS_OF_DATABASE",
    database = "DATABASE_NAME"
)


def insertData(datetime, minimum, maximum, volume, percentChange):
    mycursor = mydb.cursor()
    sql = "INSERT INTO SHIB_data (timestamp, min, max, volume, percentChange) VALUES (%s, %s, %s, %s, %s)"
    val = (datetime, minimum, maximum, volume, percentChange)
    mycursor.execute(sql, val)
    mydb.commit()



## current table reference
# | Field         | Type     | Null | Key | Default | Extra |
# +---------------+----------+------+-----+---------+-------+
# | timestamp     | datetime | YES  |     | NULL    |       |
# | min           | float    | YES  |     | NULL    |       |
# | max           | float    | YES  |     | NULL    |       |
# | volume        | float    | YES  |     | NULL    |       |
# | percentChange | float    | YES  |     | NULL    |       |

### GateIO API response Structure
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