#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://localhost:8080"

    values_to_set = {
        "EngineInfo.EngineName": "New Engine Name", 
        "EngineInfo.Location.Latitude": 41.888332,   
        "EngineInfo.Location.Longitude": -87.602566 }

    engine = Engine.fromurl(address)

    print(f"Settings {len(values_to_set)} values...")
    engine.set_current_data_values(values_to_set)
    print("done.")


if __name__ == '__main__':
    main(args=sys.argv)
