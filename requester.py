import json
import os
from datetime import datetime
from urllib.parse import urljoin

import requests


class Requester:

    API_TOKEN = '2ba07897-5c23-405c-9633-3b6197a07ab5'
    API_GAME_TOKEN = '3d08a8ba-830b-4a30-8f43-6a0f2cc0c03b'
    BASE_URL = 'https://open.faceit.com/data/v4/'
    BASE_URL_V2 = 'https://api.faceit.com/match-history/v4/matches/competition'
    MATCH_INFO_URL = 'matches/'
    GAME_ID = 'csgo'

    def get(self, url):
        headers = {
            'Authorization': f'Bearer {self.API_TOKEN}',
            'Accept': 'application/json'
        }
        url = urljoin(self.BASE_URL, url)
        response = requests.get(url, headers=headers)
        return response.content

    def _get(self, url):
        response = requests.get(url)
        return response.content

    def get_matches(self, page):
        headers = {
            'Authorization': f'Bearer {self.API_GAME_TOKEN}',
            'Accept': 'application/json'
        }
        params = {
            'id': '42e160fc-2651-4fa5-9a9b-829199e27adb',
            'page': page,
            'size': 1000,
            'type': 'matchmaking'
        }
        url = urljoin(self.BASE_URL, self.BASE_URL_V2)
        response = requests.get(url, headers=headers, params=params)
        return response.content

    def get_player_stats(self, player_id):
        return self.get(f'players/{player_id}/stats/csgo')

    def get_player_details(self, player_id):
        return self.get(f'players/{player_id}')

    def download_demo(self, match_id):
        match_info = json.loads(self.get(f'{self.MATCH_INFO_URL}/{match_id}'))
        demo_url = match_info['demo_url'][0]
        start = datetime.now()
        with open('match.dem.gz', 'wb') as demo_file:
            demo_file.write(self._get(demo_url))
        end = datetime.now()
        print(f'Demo downloaded: "{match_id}". Size: {int(os.path.getsize("match.dem.gz") / 1024 / 1024)} MB. '
              f'Time: {end - start}')
