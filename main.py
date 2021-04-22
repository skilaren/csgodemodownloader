import logging
import threading

from requests.exceptions import HTTPError

from player_info import get_player_info, Player
from requester import Requester


logger = logging.getLogger(__name__)


def load_players(start, end):
    r = Requester()

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

    for i in range(start, end):
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
                logger.warning(match['matchId'])
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
                            logger.warning(f'{player_info.nickname:20} {player_info.rank:3} {player_info.elo:5}')
                            ranks_players[player_info.rank] += 1
                            counter += 1
                            break
                        except KeyError:
                            logger.warning(f'Player "{player}" has no CS in his games')
                            break
                        except HTTPError:
                            logger.warning(f'HTTPError')
                            continue
                logger.warning(counter)
                if counter > 1000:
                    break


if __name__ == '__main__':
    for j in range(11, 101, 10):
        thread = threading.Thread(target=load_players, args=(j - 10, j))
        thread.start()
        logger.warning(f'thread {j} started')
