from client import diagnose


def getExampleData():
    Opts = dict({"path": "/wip/prognose", "query": "source=Battery01"})

    data = diagnose(Opts)

    if(data['response'] == []):
        raise Exception("no data received")
    return data['response']


data = getExampleData()
print(f"received {len(data)} data sets")
