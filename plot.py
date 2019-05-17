from datetime import datetime
import json

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

