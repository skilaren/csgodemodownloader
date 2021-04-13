class Grenade:

    def __init__(self, thrower, trajectory, g_round):
        self.thrower = thrower
        self.trajectory = trajectory
        self.g_round = g_round


class Flash(Grenade):

    def __init__(self, thrower, effective, trajectory, g_round):
        super(Flash, self).__init__(thrower, trajectory, g_round)
        self.effective = effective
        self.total_duration = 0

    def add_flash_duration(self, duration):
        self.total_duration += duration

    def __str__(self):
        return f'Flash by "{self.thrower}" in round: {self.g_round}, duration: {self.total_duration}'


class Smoke(Grenade):

    def __init__(self, thrower, trajectory, g_round):
        super(Smoke, self).__init__(thrower, trajectory, g_round)
        self.desc = 'Smoke'

    def __str__(self):
        return f'Smoke by "{self.thrower}" in round: {self.g_round}'


class HE(Grenade):

    def __init__(self, thrower, effective, trajectory, g_round, unique_id):
        super(HE, self).__init__(thrower, trajectory, g_round)
        self.effective = effective
        self.total_damage = 0
        self.unique_id = unique_id
        self.desc = 'HE'

    def add_damage(self, damage):
        self.total_damage += damage

    def __str__(self):
        return f'HE by "{self.thrower}" in round: {self.g_round}'
