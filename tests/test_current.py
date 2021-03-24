import sys
from solutionfamily.engine import Engine
import os

def main(args=[]):
#    address = "http://192.168.0.14:8080"
    address = ""

    engine = Engine.fromurl(address)

    current_dir = os.path.dirname(os.path.realpath(__file__))

    with open(f'{current_dir}\\current_1.xml', 'r') as file:
        xml = file.read()

    # python name mangling of private functions
    t = engine._Engine__get_current_value_from_xml("SerialPort.Faulted", xml)

    print(t)

if __name__ == '__main__':
    main(args=sys.argv)
