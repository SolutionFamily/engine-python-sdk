#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

import time

# http://172.31.240.197:25008/api/engine/dataitems
def main(args=[]):
    address = "http://192.168.0.14:8080"
#    address = "http://localhost:8080"
    item_ids = ['EngineInfo.ProcessorLoadPct', 'EngineInfo.UpTime']

    # create the engine
    engine = Engine.fromurl(address)

    query_individual = False

    while True:

        if query_individual:
            for id in item_ids:
                val = engine.get_current_value(id)
                print(f"{id} = {val}")
            pass
        else:
            # query all values in the `item_ids` list
            # this is only supported in newer Engine builds catch and fallback if necessary
            try:
                values = engine.get_current_data_values(item_ids)

                # we get back a dictionary of the values
                for v in values:
                    print(f"{v} = {values[v]}")
            except EnvironmentError:
                print(f'Engine version: {engine.version} - falling back to individual item query...')
                query_individual = True


        # wait and loop
        print("----")
        time.sleep(5)

if __name__ == '__main__':
    main(args=sys.argv)
