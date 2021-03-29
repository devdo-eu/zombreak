from cpu_player_shelter import CPUPlayerShelter
from game_state import GameState
from supply_enums import Supply
import pytest


@pytest.fixture
def game():
    gs = GameState()
    gs.setup_game(['CPU', 'Other'])
    gs.players[0] = CPUPlayerShelter('CPU')
    gs.active_player = gs.players[0]
    return gs


def test_cpu_player_shelter_ctor():
    shelter = CPUPlayerShelter('Example Name')
    assert shelter.name == 'Example Name'
    assert shelter.gui == shelter.cpu_ui
    assert shelter.input == shelter.cpu_input


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

