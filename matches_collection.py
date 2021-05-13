import json

from player_info import Player, get_player_info
from requester import Requester

r = Requester()

counter = 0
for i in range(1):
    match_history = r.get_matches(page=i)['payload']
    for match in match_history:
        print(f'matchId: {match["matchId"]}')
        players = match['playingPlayers']
        for player in players:
            print(f'Player "{player}" started')
            player_stats = get_player_info(r.get_player_stats(player))
            if not player_stats:
                print(f'Player "{player}" has no CS in his games')
                continue
            player_details = r.get_player_details(player)

            try:
                player_info = Player(
                    stats=player_stats,
                    nickname=player_details['nickname'],
                    rank=player_details['games']['csgo']['skill_level'],
                    id=player,
                    elo=player_details['games']['csgo']['faceit_elo'],
                    faceit_id=player_details['player_id']
                )
            except KeyError:
                print(f'Player "{player}" has no CS in his games')
            else:
                print(f'Player "{player}" matches loading started')
                if player_info.save_to_db_faceit_stats():
                    player_info.load_matches_to_db_and_celery()
                counter += 1
                print(f'Player "{player}" matches loading finished')
        print(counter)
