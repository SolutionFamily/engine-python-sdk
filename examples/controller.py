#!/usr/bin/env python3

import sys
import time
from time import sleep
from datetime import datetime

# Import Engine from our solutionfamily.engine package
from solutionfamily.engine import Engine

def main(args=[]):

	#Define the location for our LIMS Box
    address = "http://localhost:8080"

    #Create the Engine to the LIMS Box
    engine = Engine.fromurl(address)
    start = time.time()
    print(f'Python Controller Connected...')
    print(f'  Querying Engine Structure...')

    #Query the engine
    engine.refresh_info()

    print(f'*******************************')
    print(f'  Name: {engine.name}')
    print(f'  Version: {engine.version}')
    print(f'  Host OS: {engine.hostOS}')
    print(f'  Python: {sys.version}')

    emergency = False
    while True:

        # Read the current value
        currentValue = engine.get_current_value("Facility.Temp")

        # Threshold the current value
        dValue = float(currentValue.value)
        if  dValue > 42 and emergency == False:
        	print(f'{datetime.now()} - Emergency!!! Temp ==> {dValue}')
        	emergency = True
        	engine.set_current_data_value("Facility.Emergency", True)
        else:
        	if dValue <= 42 and emergency == True:
        		print(f'{datetime.now()} - Emergency Cleared... Temp ==> {dValue}')
        		engine.set_current_data_value("Facility.Emergency", False)
        		emergency = False

       	# Sleep 
        time.sleep(1)
 
if __name__ == '__main__':
    main(args=sys.argv)

