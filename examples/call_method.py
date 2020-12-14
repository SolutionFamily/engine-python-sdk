#!/usr/bin/env python3

import sys
from solutionfamily.engine import Engine

def main(args=[]):
    address = "http://localhost:8080"

    engine = Engine.fromurl(address)

    print(f"Calling Engine method...")
    engine.invoke_method('EngineInfo', 'RestartEngine')
    print("done.")


if __name__ == '__main__':
    main(args=sys.argv)

