import xml.etree.ElementTree as ET
import requests
import dateutil.parser
from datetime import datetime
import collections
import json

# pip requirements:
#install lxml
#install requests
#install python-dateutil

class Engine:
    #This is effectively a static in python
    ns = {'mtc': 'urn:mtconnect.com:MTConnectDevices:1.1', 's': 'urn:mtconnect.com:MTConnectStreams:1.1'}
    
    def __init__(self, path):
        self.url = path
        self.devices = []
        self.__Methods = []
        self.__build = None
        self.version = '<unknown>'
        self.hostOS = '<unknown>'
        self.name = '<unknown>'

    @staticmethod
    def fromurl(path):
        engine = Engine(path)
        return engine

    def __getitem__(self, key):
        return next((d for d in self.devices if d.name == key), None)

    def refresh_info(self):
        # use an MTConnect query, as they don't require v4 APIs
        self.version = self.get_current_value('EngineInfo.VersionNumber')
        self.__build = int(self.version.split('.')[2])
        self.hostOS = self.get_current_value('EngineInfo.HostOS')
        self.name = self.get_current_value('EngineInfo.EngineName')

    def refresh_structure(self):
        self.__loadmethods(self.url)
        self.__loaddevices(self.url)

    def get_current_value(self, dataItemId):
        # {{engine_root}}/mtc/current?path=//DataItem[@id="{id}"]
        # expected return looks like:
        # <MTConnectStreams xmlns="urn:mtconnect.com:MTConnectStreams:1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:mtconnect.com:MTConnectStreams:1.1 http://www.mtconnect.org/schemas/MTConnectStreams_1.1.xsd">
        # <Header creationTime="2021-03-18T23:30:44" sender="RevPi40109" instanceId="637517062788184740" bufferSize="10000" version="4.0.21073.0" nextSequence="55751" firstSequence="488" lastSequence="488" />
        # <Streams>
        #    <DeviceStream uuid="EngineInfo" id="EngineInfo" name="EngineInfo">
        #    <Events>
        #        <Other dataItemId="EngineInfo.VersionNumber" sequence="488" timestamp="2021-03-18T19:17:53" name="VersionNumber">4.0.21073.0</Other>
        #    </Events>
        #</DeviceStream>
        #</Streams>
        #</MTConnectStreams>
        response = requests.get(f'{self.url}/mtc/current?path=//DataItem[@id=\"{dataItemId}\"]')
        tree = ET.fromstring(response.content)
        streams = tree.find('s:Streams', Engine.ns)
        if streams:
            device = streams.find('s:DeviceStream', Engine.ns)
            if device:
                # is this a device or component? MTConnect, sigh
                comp = device.find('s:ComponentStream', Engine.ns)

                if not comp is None:
                    for strm in comp.getchildren():
                        for di in strm.getchildren():
                            if di.attrib['dataItemId']==dataItemId:
                                return di.text
                else:
                    for strm in device.getchildren():
                        for di in strm.getchildren():
                            if di.attrib['dataItemId']==dataItemId:
                                return di.text

        return None

    def set_current_value(self, dataItemId, value):
        # {{engine_root}}/mtc/current?path=//DataItem[@id="{id}"]
        # expected return looks like:
        # <MTConnectStreams xmlns="urn:mtconnect.com:MTConnectStreams:1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:mtconnect.com:MTConnectStreams:1.1 http://www.mtconnect.org/schemas/MTConnectStreams_1.1.xsd">
        # <Header creationTime="2021-03-18T23:30:44" sender="RevPi40109" instanceId="637517062788184740" bufferSize="10000" version="4.0.21073.0" nextSequence="55751" firstSequence="488" lastSequence="488" />
        # <Streams>
        #    <DeviceStream uuid="EngineInfo" id="EngineInfo" name="EngineInfo">
        #    <Events>
        #        <Other dataItemId="EngineInfo.VersionNumber" sequence="488" timestamp="2021-03-18T19:17:53" name="VersionNumber">4.0.21073.0</Other>
        #    </Events>
        #</DeviceStream>
        #</Streams>
        #</MTConnectStreams>
        response = requests.get(f'{self.url}/mtc/current?path=//DataItem[@id=\"{dataItemId}\"]')
        tree = ET.fromstring(response.content)
        streams = tree.find('s:Streams', Engine.ns)
        if streams:
            device = streams.find('s:DeviceStream', Engine.ns)
            if device:
                for strm in device.getchildren():
                    for di in strm.getchildren():
                        if di.attrib['dataItemId']==dataItemId:
                            return di.text

        return None

    def get_current_data_values(self, values):
        if self.__build == None:
            self.refresh_info()

        if self.__build < 20348:
            raise EnvironmentError('Engine version 4.0.20438 or later required for get_current_data_values().  Use get_current_value()')

        # this is a v4 API and requires newer Engines (4.0.20348 and later)
        response = requests.request(method="get", url=f"{self.url}/api/engine/dataitems", data=json.dumps(values))
        return response.json()

    def set_current_data_values(self, values):
        if self.__build == None:
            self.refresh_info()

        if self.__build < 20348:
            itemsnode = ET.Element('DataItems')
            for di in values:
                itemnode = ET.SubElement(itemsnode, 'DataItem')
                itemnode.set('dataItemId', di)
                valuenode = ET.SubElement(itemnode, 'Value')
                valuenode.text = str(values[di])

            content = ET.tostring(itemsnode)
            response = requests.post(f"{self.url}/agent/data", content)
            if(response.status_code != 200):            
                return False
            return True

        else:
            # this is a v4 API and requires newer Engines (4.0.20348 and later)
            response = requests.request(method="put", url=f"{self.url}/api/engine/dataitems", data=json.dumps(values))
            if(response.status_code != 200):            
                return False
            return True

    def invoke_method(self, adapter_id, method_name, params = None):
        # this is a legacy version, but allows for older Engine support
        """
        POST to [url]/agent/adapters/{adapterID}
        <CallMethod methodName="Start">
            <Parameter name="{paramName}>{paramValue}</Parameter>
        </Callmethod>
       
        """
        callnode = ET.Element('CallMethod')
        callnode.set('methodName', method_name)
        if params:
            for p in params:
                pnode = ET.SubElement(callnode, 'Parameter')
                pnode.set('name', p.name)
                pnode.text = p.value

        path = self.url + '/agent/adapters/' + adapter_id
        data = ET.tostring(callnode)
        response = requests.put(path, data)

        #update the locally-known value on success
        if(response.status_code != 200):            
            return False
        return True

    def __loadmethods(self, path):
        # we separately load all adapter methods
        response = requests.get(path + '/agent/adapters')
        tree = ET.fromstring(response.content)
        list = []
        for a in tree.findall('Adapter'):
            deviceid = a.get('deviceID')
            # does the adapter have methods?
            methods = a.find('Methods')
            if methods:
                for m in methods.findall('Method'):
                    name = m.get('name')
                    component = m.get('component')
                    returnType = m.get('returnType')
                    adapterid = m.get('adapterName')
                    method = Method(path, adapterid, deviceid, m)
                    list.append(method)
                self.__Methods = list

    def __loaddevices(self, path):
        response = requests.get(path + '/mtc/probe')        
        tree = ET.fromstring(response.content)
        list = []
        devices = tree.find('mtc:Devices', Engine.ns)
        for device in devices.findall('mtc:Device', Engine.ns):
            d = Device(self, path, device)
            d._fillMethods(self.__Methods)
            list.append(d)
        self.devices = list

class DataItemList():
    def __init__(self):
        self.__dataItems = []

    def _add(self, value):
        self.__dataItems.append(value)

    def __getitem__(self, key):
        # look by name
        di = next((d for d in self.__dataItems if d.name == key), None)

        if not di is None:
            return di

        # then by id
        return next((d for d in self.__dataItems if d.id == key), None)

class Node:
    def __init__(self, engine, path, element):
        self.__engine = engine
        self._path = path
        self.name = element.get('name')
        self.id = element.get('id')
        self.components = []
        self.dataItems = DataItemList()
        self.methods = []

    def __getitem__(self, key):
        return next((c for c in self.components if c.name == key), None)

    def _getDataItems(self, path, element):
        dataitems = element.find('mtc:DataItems', Engine.ns)
        if dataitems:
            for dataitem in dataitems.findall('mtc:DataItem', Engine.ns):
                di = DataItem(self.__engine, path, dataitem)
                self.dataItems._add(di)

    def _getComponents(self, path, element):
        cmps = element.find('mtc:Components', Engine.ns)
        if cmps:
            clist = []
            for c in cmps.findall('mtc:Component', Engine.ns):
                clist.append(Component(self.__engine, path, c))
            self.components = clist

    def _fillMethods(self, methods):
        # find all methods with us as a parent
        for m in methods:
            if self.id == m.parent:
                self.methods.append(m)
    
class Component(Node):
    def __init__(self, engine, path, element):
        super(Component, self).__init__(engine, path, element)
        super(Component, self)._getDataItems(path, element)
        super(Component, self)._getComponents(path, element)

class Device(Node):
    def __init__(self, engine, path, element):
        super(Device, self).__init__(engine, path, element)
        self.uuid = element.get('uuid')
        super(Device, self)._getDataItems(path, element)
        super(Device, self)._getComponents(path, element)

class Parameter:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Method:
    def __init__(self, path, adapterid, deviceid, element):
        self.parameters = []
        self.name = element.get('name')
        self.returnType = element.get('returnType')
        self._path = path
        self.adapterid = adapterid

        #compose the ID
        component = element.get('component')
        if(component):
            self.parent = deviceid + '.' + component
        else:
            self.parent = deviceid

        self.id = self.parent + '.' + self.name
        self.returnType = element.get('returnType')

        #does the method have parameters?
        params = element.find('Parameters')
        if params:
            for p in params.findall('Parameter'):
                self.parameters.append(Parameter(p.get('name'), p.get('type')))

    def invoke(self, params = None):
        # this is a legacy version, but allows for older Engine support
        """
        POST to [url]/agent/adapters/{adapterID}
        <CallMethod methodName="Start">
            <Parameter name="{paramName}>{paramValue}</Parameter>
        </Callmethod>
       
        """
        callnode = ET.Element('CallMethod')
        callnode.set('methodName', self.name)
        if params:
            for p in params:
                pnode = ET.SubElement(callnode, 'Parameter')
                pnode.set('name', p.name)
                pnode.text = p.value

        path = self._path + '/agent/adapters/' + self.adapterid
        data = ET.tostring(callnode)
        response = requests.put(path, data)

        #update the locally-known value on success
        if(response.status_code != 200):            
            return False
        return True

class DataItem:
    def __init__(self, engine, path, element):
        self.__engine = engine
        self._path = path
        self.category = element.get('category')
        self.type = element.get('type')
        self.name = element.get('name')
        self.id = element.get('id')
        self.writable = element.get('writable') == 'True'
        self.valueType = element.get('valueType')
        self.value = None

    def get_current_value(self):
        return self.__engine.get_current_value(self.id)

    def _set_value_from_xml(self, value, timestamp):
        if(timestamp is None):
            self.timestamp = None
        else:
            self.timestamp = dateutil.parser.parse(timestamp)

        if value is None:
            self.value = None
        else:
            if(self.valueType == 'double'):
                self.value = float(value)
            elif(self.valueType == 'boolean'):
                self.value = bool(value)
            elif(self.valueType == 'int'):
                self.value = int(value)
            elif(self.valueType == 'dateTime'):
                self.value = dateutil.parser.parse(value)
            else:
                self.value = value
        
        return self.value
    
    def set_value(self, value):
        # this is a legacy version, but allows for older Engine support
        """
        POST to [url]/agent/data
        <DataItems>
            <DataItem dataItemId="EngineInfo.EngineLocation">
            <Value>test</Value>
            </DataItem>
        </DataItems>
        """
        if self.writable:
            datanode = ET.Element('DataItems')
            item = ET.SubElement(datanode, 'DataItem')
            item.set('dataItemId', self.id)
            valnode = ET.SubElement(item, 'Value')
            valnode.text = value

            path = self._path + '/agent/data' 
            data = ET.tostring(datanode)
            response = requests.post(path, data)

            #update the locally-known value on success
            if(response.status_code == 200):
                self.value = valnode
                self.timestamp = datetime.now()
