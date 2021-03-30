from cpu_player_shelter import CPUPlayerShelter
from game_state import GameState
from supply_enums import Supply
import pytest
from tests.common import fast_zombie, zombie, big_zombie


@pytest.fixture
def game():
    gs = GameState()
    gs.setup_game(['CPU', '1', '2', '3'])
    gs.players[0] = CPUPlayerShelter('CPU')
    gs.active_player = gs.players[0]
    return gs


def test_sanity_check():
    assert fast_zombie
    assert zombie
    assert big_zombie


def test_cpu_player_shelter_ctor():
    shelter = CPUPlayerShelter('Example Name')
    assert shelter.name == 'Example Name'
    assert shelter.gui == shelter.cpu_ui
    assert shelter.input == shelter.cpu_input


def test_use_swap(game, big_zombie):
    cpu = game.active_player
    cpu.supplies = [Supply.SWAP, Supply.AXE, Supply.AXE]
    game.players[3].obstacles = [Supply.BARRICADES, Supply.ALARM, Supply.BARRICADES, Supply.ALARM, Supply.BARRICADES]
    game.players[1].obstacles = [Supply.ALARM]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_swap()
    assert cpu.planned_moves == ['0', '2']

    game.players[3].defeated = True
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_swap()
    assert cpu.planned_moves == ['0', '0']

    cpu = game.active_player
    cpu.supplies = [Supply.SWAP, Supply.AXE, Supply.AXE]
    cpu.obstacles = [Supply.ALARM, Supply.BARRICADES]
    game.players[3].obstacles = [Supply.BARRICADES]
    game.players[3].defeated = False
    game.players[1].obstacles = [Supply.ALARM]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_swap()
    assert cpu.planned_moves == []

    cpu.planned_moves = []
    cpu.supplies = [Supply.GUN, Supply.SWAP, Supply.AXE]
    cpu.obstacles = []
    game.players[3].zombies = [big_zombie]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_swap()
    assert cpu.planned_moves == ['1', '0']

    cpu.planned_moves = []
    cpu.supplies = [Supply.GUN, Supply.AXE, Supply.SWAP]
    game.players[3].zombies = [big_zombie]
    game.players[1].zombies = [big_zombie]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_swap()
    assert cpu.planned_moves == ['2', '1']

    cpu.planned_moves = []
    cpu.supplies = [Supply.GUN, Supply.AXE, Supply.SWAP]
    game.players[3].zombies = [big_zombie]
    game.players[1].zombies = [big_zombie]
    game.players[2].zombies = [big_zombie]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_swap()
    assert cpu.planned_moves == []


def test_use_chainsaw(game):
    cpu = game.active_player
    cpu.supplies = [Supply.CHAINSAW, Supply.AXE, Supply.AXE]
    game.players[3].obstacles = [Supply.BARRICADES, Supply.ALARM]
    game.players[1].obstacles = [Supply.ALARM]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_chainsaw()
    assert cpu.planned_moves == ['0', '1']

    game.players[3].obstacles = []
    game.players[1].obstacles = []
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_chainsaw()
    assert cpu.planned_moves == ['0', '0']

    game.players[3].obstacles = [Supply.BARRICADES]
    cpu.gui(game)
    cpu.planned_moves = []
    cpu.use_chainsaw()
    assert cpu.planned_moves == ['0', '0']


def test_use_drone(game, big_zombie, fast_zombie):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.DRONE, Supply.AXE]
    cpu.zombies = [big_zombie]
    cpu.gui(game)
    cpu.use_drone()
    assert cpu.planned_moves[0] == '1'
    assert len(cpu.planned_moves) == 2

    cpu.supplies = [Supply.AXE, Supply.GUN, Supply.DRONE]
    cpu.zombies = [big_zombie, fast_zombie]
    cpu.gui(game)
    cpu.use_drone()
    assert cpu.planned_moves[0] == '2'
    assert len(cpu.planned_moves) == 3


def test_use_lure_out(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.DRONE, Supply.LURE_OUT]
    cpu.zombies = [big_zombie]
    cpu.gui(game)
    cpu.use_lure_out()
    assert len(cpu.planned_moves) == 2
    assert cpu.planned_moves[0] == '2'

    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.DRONE, Supply.LURE_OUT]
    cpu.zombies = [zombie]
    cpu.gui(game)
    cpu.use_lure_out()
    assert len(cpu.planned_moves) == 2
    assert cpu.planned_moves[0] == '2'

    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.DRONE, Supply.LURE_OUT]
    game.city_deck = [zombie]
    cpu.zombies = [big_zombie]
    cpu.gui(game)
    cpu.use_lure_out()
    assert len(cpu.planned_moves) == 4
    assert cpu.planned_moves[0] == '2'
    assert cpu.planned_moves[1] == 'y'

    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.DRONE, Supply.LURE_OUT]
    game.city_deck = [zombie]
    cpu.zombies = [big_zombie, zombie]
    cpu.gui(game)
    cpu.use_lure_out()
    assert len(cpu.planned_moves) == 5
    assert cpu.planned_moves[0] == '2'
    assert cpu.planned_moves[1] == 'y'
    assert cpu.planned_moves[3] == '0'


def test_use_sacrifice(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.SACRIFICE, Supply.AXE]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.use_sacrifice()
    assert len(cpu.planned_moves) == 5
    assert cpu.planned_moves[0] == '1'


def test_use_shotgun(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.SHOTGUN, Supply.AXE]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.use_shotgun()
    assert len(cpu.planned_moves) == 2
    assert cpu.planned_moves[0] == '1'
    assert cpu.planned_moves[1] == '0'

    cpu.zombies = [big_zombie, zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.use_shotgun()
    assert len(cpu.planned_moves) == 2
    assert cpu.planned_moves[0] == '1'
    assert cpu.planned_moves[1] == '1'

    cpu.zombies = [zombie]
    cpu.gui(game)
    cpu.use_shotgun()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == '1'


def test_use_sniper(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.SACRIFICE, Supply.SNIPER]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.use_sniper()
    assert len(cpu.planned_moves) == 2
    assert cpu.planned_moves[0] == '2'

    game.city_deck = [zombie]
    cpu.gui(game)
    cpu.use_sniper()
    assert len(cpu.planned_moves) == 2
    assert cpu.planned_moves[0] == '2'
    assert cpu.planned_moves[1] == 'y'

    cpu.use_sniper(defend=True)
    assert len(cpu.planned_moves) == 3
    assert cpu.planned_moves[0] == '2'
    assert cpu.planned_moves[1] == 'n'


def test_defend_with_barricades(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.obstacles = [Supply.BARRICADES, Supply.BARRICADES]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_barricades()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'y'

    cpu.obstacles = [Supply.BARRICADES]
    cpu.zombies = [big_zombie]
    cpu.gui(game)
    cpu.defend_with_barricades()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'y'

    cpu.obstacles = [Supply.BARRICADES, Supply.MINE_FILED, Supply.MINE_FILED]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_barricades()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'n'

    cpu.obstacles = [Supply.BARRICADES, Supply.ALARM]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_barricades()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'n'


def test_defend_with_alarm(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.obstacles = [Supply.ALARM, Supply.BARRICADES]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_alarm()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'y'

    cpu.obstacles = [Supply.ALARM, Supply.MINE_FILED, Supply.MINE_FILED]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_alarm()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'n'

    cpu.obstacles = [Supply.ALARM, Supply.BARRICADES, Supply.BARRICADES]
    cpu.zombies = [big_zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_alarm()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'n'

    cpu.obstacles = [Supply.ALARM, Supply.BARRICADES, Supply.BARRICADES]
    cpu.zombies = [big_zombie, big_zombie, zombie]
    cpu.gui(game)
    cpu.defend_with_alarm()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'y'


def test_defend_wit_mine_field(game, big_zombie, zombie):
    cpu = game.active_player
    cpu.obstacles = [Supply.ALARM, Supply.MINE_FILED, Supply.MINE_FILED]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_mine_field()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'y'

    cpu = game.active_player
    cpu.obstacles = [Supply.MINE_FILED, Supply.ALARM]
    cpu.zombies = [big_zombie, big_zombie, zombie, big_zombie]
    cpu.gui(game)
    cpu.defend_with_mine_field()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'n'

    cpu = game.active_player
    cpu.obstacles = [Supply.MINE_FILED, Supply.BARRICADES]
    cpu.zombies = [big_zombie]
    cpu.gui(game)
    cpu.defend_with_mine_field()
    assert len(cpu.planned_moves) == 1
    assert cpu.planned_moves[0] == 'y'
