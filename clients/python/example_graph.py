try:
    import pandas as pd
    import plotly.graph_objects as go
except:
    print("please uncomment pandas and plotly from requirements and do 'pip install -r requirements.txt'")
    exit(1)

from example import getExampleData

data = getExampleData()

health = {}
cycle = {}

for d in data:
    if d['aggregator'] == "cycles":
        cycle = d['data']
    if d['aggregator'] == "health":
        health = d['data']

df1 = pd.DataFrame.from_dict(health)
df2 = pd.DataFrame.from_dict(cycle)

fig = go.Figure([go.Scatter(x=df2['value'], y=df1['value'])])
fig.update_layout(title="health vs cycle")
fig.show()
