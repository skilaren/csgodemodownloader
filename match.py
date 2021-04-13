class Rounds:

    T_TEAM = 2
    CT_TEAM = 3

    def __init__(self):
        self.t1_score = 0
        self.t2_score = 0
        self.knife_round = True

    def round_end(self, winner):
        if winner == self.CT_TEAM:
            if self.sum() < 15:
                self.t1_score += 1
            elif self.sum() < 30:
                self.t2_score += 1
            else:
                if ((self.sum() - 30) / 3) % 2 == 0:
                    self.t2_score += 1
                else:
                    self.t1_score += 1
        if winner == self.T_TEAM:
            if self.sum() < 15:
                self.t2_score += 1
            elif self.sum() < 30:
                self.t1_score += 1
            else:
                if ((self.sum() - 30) / 3) % 2 == 0:
                    self.t1_score += 1
                else:
                    self.t2_score += 1

    def sum(self):
        return self.t1_score + self.t2_score

    def __str__(self):
        return f'T1 {self.t1_score} : {self.t2_score} T2'
