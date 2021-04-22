import sys

from requests.exceptions import HTTPError

from player_info import get_player_info, Player
from requester import Requester


if __name__ == '__main__':
    _, start, begin = sys.argv
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

    for i in range(int(start), int(begin)):
        with open(f'results{start}.csv', mode='w+') as res_file:
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
            match_history = r.get_matches(page=i)['payload']
            for match in match_history:
                print(match['matchId'])
                players = match['playingPlayers']
                for player in players:
                    while True:
                        try:
                            player_stats = get_player_info(r.get_player_stats(player))
                            player_details = r.get_player_details(player)
                            player_info = Player(
                                stats=player_stats,
                                nickname=player_details['nickname'],
                                rank=player_details['games']['csgo']['skill_level'],
                                id=player,
                                elo=player_details['games']['csgo']['faceit_elo'],
                                faceit_id=''
                            )
                            res_file.write(player_info.to_csv())
                            print(f'{player_info.nickname:20} {player_info.rank:3} {player_info.elo:5}')
                            ranks_players[player_info.rank] += 1
                            counter += 1
                            break
                        except KeyError:
                            print(f'Player "{player}" has no CS in his games')
                            break
                        except HTTPError:
                            print(f'HTTPError')
                            continue
                print(counter)
                if counter > 1000:
                    break
