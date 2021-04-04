import json
from dataclasses import dataclass

allowed_maps = {
    'de_mirage', 'de_train', 'de_dust2', 'de_overpass', 'de_cache', 'de_nuke', 'de_vertigo', 'de_inferno', 'de_cbble'
}


@dataclass
class PlayerStats:
    assists: float = 0
    deaths: float = 0
    headshots: float = 0
    kills: float = 0
    mvps: float = 0
    penta_kills: float = 0
    quadro_kills: float = 0
    triple_kills: float = 0
    kd: float = 0
    wins: float = 0
    matches: int = 0
    rounds: int = 0

    def __str__(self):
        return json.dumps({
            'Average Assists': self.assists / self.matches,
            'Average Deaths': self.deaths / self.matches,
            'Average Headshots %': self.headshots / self.kills,
            'Headshots per Match': self.headshots / self.matches,
            'K/D Ratio': self.kills - self.deaths,
            'K/D Ratio (%)': self.kills / self.deaths,
            'K/R Ratio': self.kills / self.rounds,
            'Average Kills': self.kills / self.matches,
            'Average MVPs': self.mvps / self.matches,
            'Average Penta Kills': self.penta_kills / self.matches,
            'Average Quadro Kills': self.quadro_kills / self.matches,
            'Average Triple Kills': self.triple_kills / self.matches,
            'Matches': self.matches,
            'Wins': self.wins,
            'Winrate': self.wins / self.matches,
            'Rounds': self.rounds
        })

    def to_csv(self):
        return f'{self.assists / self.matches},' \
               f'{self.deaths / self.matches},' \
               f'{(self.headshots / self.kills) if self.kills else "NaN"},' \
               f'{self.headshots / self.matches},' \
               f'{self.kills - self.deaths},' \
               f'{self.kills / self.deaths},' \
               f'{self.kills / self.rounds},' \
               f'{self.kills / self.matches},' \
               f'{self.mvps / self.matches},' \
               f'{self.penta_kills / self.matches},' \
               f'{self.quadro_kills / self.matches},' \
               f'{self.triple_kills / self.matches},' \
               f'{self.matches},' \
               f'{self.wins},' \
               f'{self.wins / self.matches},' \
               f'{self.rounds}'

    @property
    def kd_ratio(self):
        return self.kills / self.deaths

    @property
    def kd_ratio(self):
        return self.kills / self.deaths


@dataclass
class Player:

    stats: PlayerStats
    rank: int
    nickname: str
    id: str
    elo: int

    def to_csv(self):
        return f'{self.stats.to_csv()},{self.rank},{self.elo},{self.nickname}\n'


def get_player_info(stats_json):
    player_stats = PlayerStats()
    maps = stats_json['segments']
    for _map in maps:
        if _map['label'] in allowed_maps:
            stats = _map['stats']
            player_stats.assists += int(stats['Assists'])
            player_stats.deaths += int(stats['Deaths'])
            player_stats.headshots += int(stats['Headshots'])
            player_stats.kills += int(stats['Kills'])
            player_stats.mvps += int(stats['MVPs'])
            player_stats.penta_kills += int(stats['Penta Kills'])
            player_stats.quadro_kills += int(stats['Quadro Kills'])
            player_stats.triple_kills += int(stats['Triple Kills'])
            player_stats.wins += int(stats['Wins'])
            player_stats.rounds += int(stats['Rounds'])
            player_stats.matches += int(stats['Matches'])
    return player_stats
