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
    game.players[3].obstacles = [Supply.BARRICADES, Supply.ALARM]
    game.players[1].obstacles = [Supply.ALARM]
    cpu.gui(game)
    cpu.use_swap()
    assert cpu.planned_moves == ['0', '2']

    cpu.supplies = [Supply.GUN, Supply.SWAP, Supply.AXE]
    game.players[3].zombies = [big_zombie]
    cpu.gui(game)
    cpu.use_swap()
    assert cpu.planned_moves == ['1', '1']

    cpu.supplies = [Supply.GUN, Supply.AXE, Supply.SWAP]
    game.players[3].zombies = [big_zombie]
    game.players[1].zombies = [big_zombie]
    cpu.gui(game)
    cpu.use_swap()
    assert cpu.planned_moves == ['2', '0']

    cpu.supplies = [Supply.GUN, Supply.AXE, Supply.SWAP]
    game.players[3].zombies = [big_zombie]
    game.players[1].zombies = [big_zombie]
    game.players[2].zombies = [big_zombie]
    cpu.gui(game)
    cpu.use_swap()
    assert cpu.planned_moves[0] == '2'


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


def test_cpu_discard_policy(game):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.AXE, Supply.AXE]
    action, possible_actions = game.ask_player_what_move()
    assert cpu.policy['discard']
    assert action == '3'

    cpu.supplies = [Supply.AXE, Supply.AXE]
    action, possible_actions = game.ask_player_what_move()
    assert not cpu.policy['discard']
    assert cpu.policy['end_turn']
    assert action == '2'


def test_counter_summons_policy(game):
    cpu = game.active_player
    cpu.supplies = [Supply.AXE, Supply.GUN, Supply.SHOTGUN]
    action, possible_actions = game.ask_player_what_move()
    assert cpu.policy['counter_summons']
    assert action == '1'

    cpu.supplies = [Supply.AXE, Supply.SHOTGUN]
    action, possible_actions = game.ask_player_what_move()
    assert not cpu.policy['counter_summons']
    assert cpu.policy['end_turn']
    assert action == '2'
