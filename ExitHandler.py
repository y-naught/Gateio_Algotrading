# Safely closes any connections that are still open when the user exits the system

import ManageSQL
import atexit

def exitHandler():
    ManageSQL.closeConnection()
    print("Exiting the application")

atexit.register(exitHandler)