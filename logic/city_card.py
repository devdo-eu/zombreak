from enums.zombie import ZombieType


class CityCard:
    def __init__(self, zombie: ZombieType = ZombieType.ZOMBIE):
        if zombie == ZombieType.SURVIVOR:
            raise Exception('Card cannot be init with survivor on top!')
        self.active = True
        self.top = ZombieType.SURVIVOR
        self.bottom = zombie

    def flip(self) -> None:
        """Method used to flip card up side down."""
        self.top, self.bottom = self.bottom, self.top
