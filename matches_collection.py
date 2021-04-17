import json

from player_info import Player, get_player_info
from requester import Requester

r = Requester()

for i in range(10):
    counter = 0
    match_history = r.get_matches(page=i)['payload']
    for match in match_history:
        print(f'matchId: {match["matchId"]}')
        players = match['playingPlayers']
        for player in players:
            try:
                player_stats = get_player_info(r.get_player_stats(player))
                player_details = r.get_player_details(player)
                player_info = Player(
                    stats=player_stats,
                    nickname=player_details['nickname'],
                    rank=player_details['games']['csgo']['skill_level'],
                    id=player,
                    elo=player_details['games']['csgo']['faceit_elo'],
                    faceit_id=player_details['player_id']
                )
                player_info.save_to_db_faceit_stats()
                player_info.load_matches_to_db_and_celery()
                counter += 1
                if counter % 100 == 0:
                    print(counter)
            except KeyError:
                print(f'Player "{player}" has no CS in his games')
        if counter > 15000:
            break
# put all matches in celery queue

# CELERY
# load match
# parse info
# load to db
