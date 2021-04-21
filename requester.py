import uuid
import os
import gzip
import shutil
from datetime import datetime
from urllib.parse import urljoin

import requests


class Requester:

    API_TOKEN = '2ba07897-5c23-405c-9633-3b6197a07ab5'
    API_GAME_TOKEN = 'b435db82-d553-4346-86d5-b40396e2df53'
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
        return response.json()

    def _get(self, url):
        response = requests.get(url)
        return response.json()

    def get_file(self, url):
        response = requests.get(url)
        return response.content

    def get_matches(self, page):
        headers = {
            'Authorization': f'Bearer {self.API_GAME_TOKEN}',
            'Accept': 'application/json'
        }
        params = {
            'id': '42e160fc-2651-4fa5-9a9b-829199e27adb',
            'page': page + 5,
            'size': 1000,
            'type': 'matchmaking'
        }
        url = urljoin(self.BASE_URL, self.BASE_URL_V2)
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_player_stats(self, player_id):
        return self.get(f'players/{player_id}/stats/csgo')

    def get_player_details(self, player_id):
        return self.get(f'players/{player_id}')

    def get_match_stats(self, match_id, chosen_player_id):
        stats = self.get(f'matches/{match_id}/stats')['rounds'][0]
        if chosen_player_id:
            for team in stats['teams']:
                for player in team['players']:
                    if player['player_id'] == chosen_player_id:
                        return player['player_stats'], player['nickname']
        else:
            return stats

    def get_player_matches(self, player_id, matches_amount):
        matches = []
        for i in range(0, min(matches_amount, 1000), 100):
            try:
                matches_batch = self.get(f'players/{player_id}/history?game=csgo&limit=100&offset={i}&from=0')['items']
            except KeyError:
                print(f'{player_id} has no matches at offset = {i}')
            else:
                for match in matches_batch:
                    matches.append({
                        'id': match['match_id'],
                        'started': match['started_at'],
                    })
        return matches

    def download_demo(self, match_id):
        match_uuid = uuid.uuid4()
        start = datetime.now()
        if not os.path.exists(f'matches/{match_uuid}.dem.gz'):
            match_info = self.get(f'{self.MATCH_INFO_URL}/{match_id}')
            demo_url = match_info['demo_url'][0]
            with open(f'matches/{match_uuid}.dem.gz', 'wb+') as demo_file:
                demo_file.write(self.get_file(demo_url))
            with gzip.open(f'matches/{match_uuid}.dem.gz', 'rb') as f_in:
                with open(f'matches/{match_uuid}.dem', 'wb+') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        end = datetime.now()
        print(f'Demo downloaded: "{match_id}". '
              f'Size: {int(os.path.getsize(f"matches/{match_uuid}.dem.gz") / 1024 / 1024)} MB. '
              f'Time: {end - start}')
        return f'{match_uuid}'
