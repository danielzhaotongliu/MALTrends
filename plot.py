from datetime import datetime
import json
import plotly.graph_objs as go
import plotly.offline as ply

# load in the data
times = []
scores = []
scores_count = []
with open('snapshots.jl', 'r') as f:
    for line in f:
        snapshot = json.loads(line)
        time = datetime.utcfromtimestamp(snapshot['timestamp'])
        times.append(time)
        scores.append(snapshot['score'])
        scores_count.append(snapshot['score_count'])

# create traces - data collections
trace = go.Scatter(
    x = times, 
    y = scores,
    name = 'scores'
)

# pack the data
data = [trace]

# configure layout
layout = go.Layout(
    title = 'MyAnimeList Scores Trend',
    xaxis = dict(
        title = 'Date',
        showticklabels=True
    ),
    yaxis = dict(
        title = 'Score',
        showticklabels=True
    )
)

# plot as html
fig = go.Figure(data=data, layout=layout)
ply.plot(fig, filename='scores_trend.html')