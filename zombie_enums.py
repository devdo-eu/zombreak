from enum import Enum, unique


@unique
class ZombieType(Enum):
    ZOMBIE = 'zombie'
    FAST = 'fast zombie'
    BIG = 'big zombie'
    HORDE = 'horde'
    SURVIVOR = 'survivor'
