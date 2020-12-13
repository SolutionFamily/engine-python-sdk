#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

import time

def main(args=[]):
    address = "http://localhost:8080"
    item_ids = ['EngineInfo.ProcessorLoadPct', 'EngineInfo.UpTime']

    # create the engine
    engine = Engine.fromurl(address)

    while True:
        # query all values in the `item_ids` list
        values = engine.get_current_data_values(item_ids)

        # we get back a dictionary of the values
        for v in values:
            print(f"{v} = {values[v]}")

        # wait and loop
        print("----")
        time.sleep(5)

if __name__ == '__main__':
    main(args=sys.argv)
