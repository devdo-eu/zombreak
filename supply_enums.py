from enum import Enum, unique


@unique
class Supply(Enum):
    ALARM = 'alarm'
    MINE_FILED = 'mine filed'
    BARRICADES = 'barricades'
    RADIO = 'radio'
    MEGAPHONE = 'megaphone'
    FLARE_GUN = 'flare gun'
    SACRIFICE = 'sacrifice survivor'
    DRONE = 'drone'
    LURE_OUT = 'lure zombie out'
    CHAINSAW = 'chainsaw'
    TAKEOVER = 'takeover survivor'
    SWAP = 'swap shelter'
    SNIPER = 'sniper rifle'
    SHOTGUN = 'shotgun'
    GUN = 'gun'
    AXE = 'axe'


@unique
class SupplyType(Enum):
    DEFENCES = 'defences'
    SUMMONS = 'summons'
    COUNTERS = 'counters'
    WEAPONS = 'weapons'
