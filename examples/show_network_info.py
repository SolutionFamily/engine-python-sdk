#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://192.168.0.14:8080"

    print(f"Querying Engine Network Information...")
    engine = Engine.fromurl(address)
    engine.refresh_info()
    engine.refresh_structure()

    for adapter in engine["Networks"].components:
        print(f"{adapter.name} at {adapter.dataItems['IPAddress'].get_current_value()}")


if __name__ == '__main__':
    main(args=sys.argv)
