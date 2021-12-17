from client import diagnose


def getExampleData():
    Opts = dict({"path": "/wip/prognose", "query": "source=Battery01"})

    data = diagnose(Opts)

    if(data == []):
        raise Exception("no data received")
    return data


data = getExampleData()
print(f"received {len(data)} data sets")
