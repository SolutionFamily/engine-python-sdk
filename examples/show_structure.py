#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://192.168.0.14:8080"

    engine = Engine.fromurl(address)

    print(f'Querying Engine Info...')
    engine.refresh_info()
    print(f'  Name:    {engine.name}')
    print(f'  Version: {engine.version}')
    print(f'  Host OS: {engine.hostOS}')

    print(f'Querying Engine Structure...')
    engine.refresh_structure()

    # print the entire Engine structure
    for d in engine.devices:        
        print(f" _[{d.name}]")
        for di in d.dataItems:
            print(f"  | -[name: {di.name} id: {di.id} ({di.valueType}) {'writable' if (di.writable == True) else 'not writable'}]")
        for m in d.methods:
            print(f"  | -<method {m.name} in adapter [{m.adapterid}]")
        for c in d.components:
            print(f"  \\_[{c.name}]")
            for di in c.dataItems:
                print(f"    | -[name: {di.name} id: {di.id} ({di.valueType}) {('writable' if (di.writable == True) else 'not writable')}]")
        for m in d.methods:
            print(f"    | -<method {m.name} in adapter [{m.adapterid}]")
            for sc in c.components:
                print(f"    \\_[{sc.name}]")
                for di in sc.dataItems:
                    print(f"        | -[name: {di.name} id: {di.id} ({di.valueType}) {('writable' if (di.writable == True) else 'not writable')}]")
                    for m in d.methods:
                        print(f"      | -<method {m.name} in adapter [{m.adapterid}]")

if __name__ == '__main__':
    main(args=sys.argv)
