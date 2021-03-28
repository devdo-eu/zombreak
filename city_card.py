from zombie_enums import ZombieType


class CityCard:
    def __init__(self, zombie=ZombieType.ZOMBIE):
        if zombie == ZombieType.SURVIVOR:
            raise Exception('Card cannot be init with survivor on top!')
        self.active = True
        self.top = ZombieType.SURVIVOR
        self.bottom = zombie

    def flip(self):
        self.top, self.bottom = self.bottom, self.top
