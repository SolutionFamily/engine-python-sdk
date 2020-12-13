# Solution Engine Python SDK Examples

## Querying the structure of an Engine

[`show_structure.py`](show_structure.py)

```
address = "http://localhost:8080"

engine = Engine.fromurl(address)

print(f'Querying Engine Structure...')

engine.refresh_structure()

# print the entire Engine structure
for d in engine.devices:        
    print(f" _[{d.name}]")
    for di in d.dataItems:
        print(f"  | -[name: {di.name} id: {di.id} ({di.valueType}) {'writable' if (di.writable == True) else 'not writable'}]")
    for c in d.components:
        print(f"  \\_[{c.name}]")
        for di in c.dataItems:
            print(f"    | -[name: {di.name} id: {di.id} ({di.valueType}) {('writable' if (di.writable == True) else 'not writable')}]")
        for sc in c.components:
            print(f"    \\_[{sc.name}]")
            for di in sc.dataItems:
                print(f"        | -[name: {di.name} id: {di.id} ({di.valueType}) {('writable' if (di.writable == True) else 'not writable')}]")
```

### Querying current DataItem values by ID

[`watch_values.py`](watch_values.py)

```
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
```
