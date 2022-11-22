# Solution Engine Python SDK

This SDK allows applications to do basic read and write operations of Devices, Components and DataItems on a network routable Soluton Engine.

It currently uses the MTConnect-pattern API (xml-based) from Engine for all of its work.

Python 3 is required for use.

## Installing on Linux

The SDK is [availble directly from PyPI](https://pypi.org/project/solutionfamily/).

Use `pip3` to install to your environment.

```
sudo apt-get install libxslt-dev
sudo apt-get install libxml2-dev
pip3 install solutionfamily
```

If you do not have `Python3` installed use the following

```
sudo apt-get update
sudo apt install python3 idle3
```

## Installing and Testing on Windows

1. Download Python 3.10.8 (amd64) from Microsoft Store

```
> python --version
Python 3.10.8
> pip --version
pip 22.2.2 from [path to file]
> pip3 --version
pip 22.2.2 from [path to file]
> pip3 install solutionfamily
[installation output]
```

2. Verify that the library can be found:

```
> python
Python 3.10.8 (tags/v3.10.8:aaaf517, Oct 11 2022, 16:50:30) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from solutionfamily.engine import Engine
>>>
```

3. No error reported indicates it can be found, so the install worked.

4. Test the MTConnect connection point of the LIMS with a browser.  Browse to 

```
http://[your_lims_ip]:8080/mtc/probe
```

5. A well-formed XML response means you can route to the device and it is running.

6. Download and edit the `show_structure.py` Sample to match your LIMS end point (line 7)

7. Execute the sample:

```
> python .\show_structure.py
[structure output]
```

## Examples

[All Examples are available here](examples/readme.md)
