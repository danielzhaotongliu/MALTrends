from datetime import datetime
import json
import glob
import os
import sys
import re
import plotly.graph_objs as go
import plotly.offline as py

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))
# get the .jl file containing the snapshots of an anime
path = __location__ + '/*.jl'

# load in the data
data_trends = {}
mal_id = None
for file_name in glob.glob(path):
    file_list = re.findall(r'snapshots_[0-9]+\.jl', file_name)
    assert len(file_list) == 1, 'ERROR: invalid path conventions'
    mal_id = int(re.findall(r'\d+', file_list[0])[0])
    with open(file_name, 'r') as f:
        for line in f:
            snapshot = json.loads(line)
            time = datetime.utcfromtimestamp(snapshot['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            data_trends[time] = snapshot['score']
    # TODO: currently only generates the static html for one anime
    break

times = []
scores = []
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
    title = f'Scores Trend for Anime with MAL ID of {mal_id}',
    xaxis = dict(
        title = 'Date',
    ),
    yaxis = dict(
        title = 'Score',
    )
)

# plot as html
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename=f'trends_{mal_id}.html')