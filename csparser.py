import json

from demo_parser import get_flashes, get_he_grenades, deaths_with_knife, get_all_stats, get_score
from utils import group_grenades_by_player


class DemoParser:

    @staticmethod
    def parse(demo_json_file_path, chosen_player=None):
        # Read demo file
        results = {}

        # Read demo file
        with open(demo_json_file_path, encoding='utf-8') as f:
            demo = json.load(f)

        results['map_name'] = demo['header']['map']

        # Analyze flashes
        all_flashes, players = get_flashes(demo)

        flashes_info = {}
        for player, nades in group_grenades_by_player(all_flashes, players).items():
            flashes_info[player] = {}
            flashes_info[player]['flashes'] = []
            total_player_flash_duration = 0
            for nade in nades:
                total_player_flash_duration += nade.total_duration
                flashes_info[player]['flashes'].append(nade.__dict__)
            flashes_info[player]['total_duration'] = total_player_flash_duration
            flashes_info[player]['flashes_amount'] = len(nades)
            flashes_info[player]['successful_flashes_amount'] = len([x for x in nades if x.effective])

        grenades_info = {}
        all_grenades, _ = get_he_grenades(demo)
        for player, nades in group_grenades_by_player(all_grenades, players).items():
            grenades_info[player] = {}
            grenades_info[player]['grenades'] = []
            total_player_nade_damage = 0
            for nade in nades:
                total_player_nade_damage += nade.total_damage
                grenades_info[player]['grenades'].append(nade.__dict__)
            grenades_info[player]['total_damage'] = total_player_nade_damage
            grenades_info[player]['grenades_amount'] = len(nades)
            grenades_info[player]['successful_grenades_amount'] = len([x for x in nades if x.effective])

        chosen_player_id = None
        for player_id, info in players.items():
            if info['name'] == chosen_player:
                chosen_player_id = player_id
                break
        if chosen_player_id:
            results['flashes'] = flashes_info[chosen_player_id]
            del results['flashes']['flashes']
            results['grenades'] = grenades_info[chosen_player_id]
            del results['grenades']['grenades']
            results['stats'] = get_all_stats(demo)[chosen_player_id]
            results['stupid_deaths'] = deaths_with_knife(demo, players)[chosen_player_id]

        return results
