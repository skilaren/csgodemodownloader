import json
import pprint
import subprocess

from csparser import DemoParser
from player_info import get_player_info, Player
from requester import Requester

if __name__ == '__main__':

    r = Requester()
    players = {}

    ranks_players = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0
    }

    req = Requester()

    for i in range(100):
        with open(f'results{i}.csv', mode='w+') as res_file:
            res_file.write(
                'Average Assists,'
                'Average Deaths,'
                'Average Headshots,'
                'Headshots per Match,'
                'K/D Ratio,'
                'K/D Ratio (%),'
                'K/R Ratio,'
                'Average Kills,'
                'Average MVPs,'
                'Average Penta Kills,'
                'Average Quadro Kills,'
                'Average Triple Kills,'
                'Matches,'
                'Wins,'
                'Winrate,'
                'Rounds,'
                'Rank,'
                'Elo,'
                'Nickname\n'
            )
            counter = 0
            match_history = json.loads(r.get_matches(page=i))['payload']
            for match in match_history:
                print(match['matchId'])
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
                            faceit_id=player_details['faceit_id']
                        )
                        res_file.write(player_info.to_csv())
                        print(f'{player_info.nickname:20} {player_info.rank:3} {player_info.elo:5}')
                        ranks_players[player_info.rank] += 1
                        counter += 1
                    except KeyError:
                        print(f'Player "{player}" has no CS in his games')
                print(counter)
                if counter > 10000:
                    break
