import pytest
from game_state import GameState
from zombie_enums import ZombieType
from city_card import CityCard
from player_shelter import PlayerShelter


outputs = []
helper_move = [-1, -1]


@pytest.fixture
def zombie():
    ret = CityCard(ZombieType.ZOMBIE)
    ret.flip()
    return ret


@pytest.fixture
def big_zombie():
    ret = CityCard(ZombieType.BIG)
    ret.flip()
    return ret


@pytest.fixture
def fast_zombie():
    ret = CityCard(ZombieType.FAST)
    ret.flip()
    return ret


@pytest.fixture
def gs():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    return gs


def dumper_factory():
    global outputs
    outputs = []

    def dump(message):
        global outputs
        outputs.append(message)
    return dump


def helper_factory(lines, index=0):
    global helper_move
    helper_move[index] = -1

    def helper(_):
        global helper_move
        helper_move[index] += 1
        commands = lines
        return commands[helper_move[index]]

    return helper
