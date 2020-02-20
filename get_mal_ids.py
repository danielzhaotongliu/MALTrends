import time
import json
import urllib.request

seen = set(int(mal_id.strip()) for mal_id in open('checked_mal_ids.txt'))

with open('mal_ids.txt', 'w') as f:
	for i in range(1, 51):
		url = 'https://api.jikan.moe/v3/top/anime/{}/bypopularity'.format(i)
		r = urllib.request.urlopen(url)
		raw_data = r.read()
		data = json.loads(raw_data.decode('utf-8'))
		for anime in data['top']:
			if int(anime['mal_id']) not in seen:
				f.write(str(anime['mal_id']) + '\n')	
		print('Finished reading {} page'.format(i))
		time.sleep(5)
