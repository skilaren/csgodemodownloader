import pprint
import subprocess

from csparser import DemoParser
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
    file_name = req.download_demo('1-3938954f-36be-491c-8e42-017fac942a0b')
    out_file_name = f'{file_name.split(".")[0]}'
    # path = default_storage.path(file_name)
    subprocess.run(['./csminify.exe', '-demo', file_name,
                    '-format', 'json',
                    '-freq', '8',
                    '-out', out_file_name])

    result = DemoParser.parse(out_file_name, chosen_player='bwoken')
    pprint.pprint(result)
# if file_name != 'trial_demo_to_demo.dem':
#     default_storage.delete(file_name)
#     default_storage.delete(out_file_name)

# for i in range(10):
#     with open(f'results{i}.csv', mode='w+') as res_file:
#         res_file.write(
#             'Average Assists,'
#             'Average Deaths,'
#             'Average Headshots,'
#             'Headshots per Match,'
#             'K/D Ratio,'
#             'K/D Ratio (%),'
#             'K/R Ratio,'
#             'Average Kills,'
#             'Average MVPs,'
#             'Average Penta Kills,'
#             'Average Quadro Kills,'
#             'Average Triple Kills,'
#             'Matches,'
#             'Wins,'
#             'Winrate,'
#             'Rounds,'
#             'Rank,'
#             'Elo,'
#             'Nickname\n'
#         )
#         counter = 0
#         match_history = json.loads(r.get_matches(page=i))['payload']
#         for match in match_history:
#             print(match['matchId'])
#             players = match['playingPlayers']
#             for player in players:
#                 try:
#                     player_stats = get_player_info(json.loads(r.get_player_stats(player)))
#                     player_details = json.loads(r.get_player_details(player))
#                     player_info = Player(
#                         stats=player_stats,
#                         nickname=player_details['nickname'],
#                         rank=player_details['games']['csgo']['skill_level'],
#                         id=player,
#                         elo=player_details['games']['csgo']['faceit_elo']
#                     )
#                     res_file.write(player_info.to_csv())
#                     print(f'{player_info.nickname:20} {player_info.rank:3} {player_info.elo:5}')
#                     ranks_players[player_info.rank] += 1
#                     counter += 1
#                     if counter % 10 == 0:
#                         print(counter)
#                         pprint.pprint(ranks_players)
#                 except KeyError:
#                     print(f'Player "{player}" has no CS in his games')
#             if counter > 100000:
#                 break
