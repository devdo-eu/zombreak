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
    LURE_OUT = 'lure zombie out tools'
    CHAINSAW = 'chainsaw'
    TAKEOVER = 'tempting stocks'
    SWAP = 'swap shelter tools'
    SNIPER = 'sniper rifle'
    SHOTGUN = 'shotgun'
    GUN = 'gun'
    AXE = 'axe'


@unique
class SupplyType(Enum):
    DEFENCE = 'defence'
    SUMMON = 'summon'
    COUNTER = 'counter'
    WEAPON = 'weapon'
