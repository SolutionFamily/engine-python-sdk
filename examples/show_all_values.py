#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://192.168.0.14:8080"
#    address = "http://localhost:8080"

    engine = Engine.fromurl(address)

    print(f'Querying Engine Structure...')
    
    engine.refresh_structure()

    # query the data values - refreshing by device/component
    for d in engine.devices:
        print(f"------------\r\nData for {d.name}\r\n------------")
        for di in d.dataItems:
            print(f"{di.id} = {di.get_current_value()}")
        for c in d.components:
            print(f"------------\r\nData for {c.name}\r\n------------")
            for di in c.dataItems:
                print(f"{di.id} = {di.get_current_value()}")
            for sc in c.components:
                print(f"------------\r\nData for {sc.name}\r\n------------")
                for di in sc.dataItems:
                    print(f"{di.id} = {di.get_current_value()}")


if __name__ == '__main__':
    main(args=sys.argv)
