from match import Rounds


class MatchInfo:

    def __init__(self, players):
        self.players_info_round = {key: {'kills': 0, 'killed_by': None, 'assists': 0, } for key in players.keys()}
        self.players_info_overall = {key: {'kills': 0, 'deaths': 0, 'assists': 0,
                                           'damage': 0, 'kast_rounds': 0, 'f_blood': 0, 'f_death': 0,
                                           'bomb_defused': 0, 'bomb_planted': 0,
                                           '1k': 0, '2k': 0, '3k': 0, '4k': 0, '5k': 0} for key in players.keys()}
        self.players = players
        self.rounds = Rounds()
        self.first_blood = True

    def new_round(self, winner):
        for player in self.players_info_round.keys():
            player_info = self.players_info_round[player]
            # KAST info
            if player_info['kills'] > 0 or player_info['assists'] > 0 or not player_info['killed_by'] or \
                    self.players_info_round[player_info['killed_by']]['killed_by']:
                self.players_info_overall[player]['kast_rounds'] += 1
            # Stats for HLTV 2.0 rating
            if player_info['kills'] > 0:
                self.players_info_overall[player][f'{player_info["kills"]}k'] += 1
        self.players_info_round = {key: {'kills': 0, 'killed_by': None, 'assists': 0, } for key in self.players.keys()}
        self.rounds.round_end(winner)
        self.first_blood = True

    def add_kill(self, player):
        self.players_info_round[player]['kills'] += 1
        self.players_info_overall[player]['kills'] += 1
        if self.first_blood:
            self.players_info_overall[player]['f_blood'] += 1
            self.first_blood = False

    def add_assist(self, player):
        self.players_info_round[player]['assists'] += 1
        self.players_info_overall[player]['assists'] += 1

    def add_death(self, victim, killer):
        self.players_info_round[victim]['killed_by'] = killer
        self.players_info_overall[victim]['deaths'] += 1
        if self.first_blood:
            self.players_info_overall[victim]['f_death'] += 1

    def add_damage(self, player, damage):
        self.players_info_overall[player]['damage'] += damage

    def add_bomb_planted(self, player):
        self.players_info_overall[player]['bomb_planted'] += 1

    def add_bomb_defused(self, player):
        self.players_info_overall[player]['bomb_defused'] += 1

    def count_hltv(self):
        rounds = self.rounds.sum()
        for player in self.players_info_overall.keys():
            kills = self.players_info_overall[player]['kills']
            deaths = self.players_info_overall[player]['deaths']
            mk1 = self.players_info_overall[player]['1k']
            mk2 = self.players_info_overall[player]['2k']
            mk3 = self.players_info_overall[player]['3k']
            mk4 = self.players_info_overall[player]['4k']
            mk5 = self.players_info_overall[player]['5k']

            avg_kill_per_round = 0.679
            avg_survive_per_round = 0.317
            avg_rmk = 1.277

            kill_rating = kills / rounds / avg_kill_per_round
            survival_rating = (rounds - deaths) / rounds / avg_survive_per_round
            rmk_rating = (mk1 + 4 * mk2 + 9 * mk3 + 16 * mk4 + 25 * mk5) / rounds / avg_rmk

            hltv_rating = (kill_rating + 0.7 * survival_rating + rmk_rating) / 2.7

            self.players_info_overall[player]['hltv_rating'] = hltv_rating

    def count_kast(self):
        rounds = self.rounds.sum()
        for player in self.players_info_overall.keys():
            self.players_info_overall[player]['kast'] = self.players_info_overall[player]['kast_rounds'] / rounds * 100

    def count_adr(self):
        rounds = self.rounds.sum()
        for player in self.players_info_overall.keys():
            self.players_info_overall[player]['adr'] = self.players_info_overall[player]['damage'] / rounds

    def count_some(self):
        rounds = self.rounds.sum()
        for player in self.players_info_overall.keys():
            self.players_info_overall[player]['kr_ratio'] = self.players_info_overall[player]['kills'] / rounds
            self.players_info_overall[player]['kd_ratio'] = self.players_info_overall[player]['kills'] / self.players_info_overall[player]['deaths']

    def get_stats(self):
        self.count_hltv()
        self.count_kast()
        self.count_adr()
        return self.players_info_overall
