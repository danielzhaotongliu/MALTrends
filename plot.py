from datetime import datetime
import json
import plotly.graph_objs as go
import plotly.offline as py

# load in the data
data_trends = {}
times = []
scores = []
with open('snapshots.jl', 'r') as f:
    for line in f:
        snapshot = json.loads(line)
        time = datetime.utcfromtimestamp(snapshot['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        data_trends[time] = snapshot['score']

for time, score in sorted(data_trends.items()):
    times.append(time)
    scores.append(score)

# create traces - data collections
trace = go.Scatter(
    x = times, 
    y = scores,
    name = 'scores',
    mode = 'lines+markers'
)

# pack the data
data = [trace]

# configure layout
layout = go.Layout(
    title = 'MyAnimeList Scores Trend',
    xaxis = dict(
        title = 'Date',
    ),
    yaxis = dict(
        title = 'Score',
    )
)

# plot as html
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='scores_trend.html')