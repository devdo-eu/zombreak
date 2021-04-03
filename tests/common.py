import pytest
from logic.game_state import GameState
from enums.zombie import ZombieType
from logic.city_card import CityCard
from player.player_shelter import PlayerShelter
import uvicorn
from multiprocessing import Process
from time import sleep
from zombreak_server import app


outputs = []
helper_move = [-1, -1]
address = '127.0.0.1:5000'


def serve(host, port):
    uvicorn.run(app, host=host, port=port)


@pytest.fixture(scope='session')
def server():
    proc = Process(target=serve, args=(address.split(":")[0], int(address.split(":")[1])), daemon=True)
    proc.start()
    sleep(0.5)
    yield
    proc.kill()


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
