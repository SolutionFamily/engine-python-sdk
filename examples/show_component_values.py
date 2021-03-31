#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://192.168.0.14:8080"
    componentID = "EngineInfo"

    engine = Engine.fromurl(address)

    print(f'Finding component...')
    
    engine.refresh_structure()

    # find the component of interest
    component = engine.find_component(componentID)

    # iterate, including any component children
    if component is None:
        print(f"No component with ID {componentID} found")
    else:
        print(f"------------\r\nData for {component.name}\r\n------------")
        for di in component.dataItems:
            print(f"{di.id} = {di.get_current_value()}")

        for c in component.components:
            print(f"------------\r\nData for {c.name}\r\n------------")
            for di in c.dataItems:
                print(f"{di.id} = {di.get_current_value()}")

            for sc in c.components:
                print(f"------------\r\nData for {sc.name}\r\n------------")
                for di in sc.dataItems:
                    print(f"{di.id} = {di.get_current_value()}")


if __name__ == '__main__':
    main(args=sys.argv)
