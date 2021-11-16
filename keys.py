## rename this file to "keys.py" 
## this is where you would place your API Key from Gate.io
import os
from dotenv import load_dotenv

load_dotenv()

myKey = os.getenv("GATE_KEY")
mySecret = os.getenv("GATE_SECRET")
myKeySecret = {"apiKey":myKey,"secretKey":mySecret}