#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://192.168.0.14:8080"

    # these data items might not exist in your engine.  Adjust as appropriate
    values_to_set = {
        "EngineInfo.EngineName": "Python Engine Name", 
        "Facility.Temperature": 42.42,   
        "Facility.Start": False }

    engine = Engine.fromurl(address)

    print(f"Settings {len(values_to_set)} values...")
    engine.set_current_data_values(values_to_set)
    print("done.")


if __name__ == '__main__':
    main(args=sys.argv)
