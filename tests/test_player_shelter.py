from player_shelter import PlayerShelter
from game_state import GameState
from city_card import CityCard
from tests.common import zombie, fast_zombie, big_zombie, dumper_factory
import tests.common
from supply_enums import Supply


def test_sanity_check():
    assert fast_zombie
    assert zombie
    assert big_zombie


def test_player_shelter_class():
    shelter = PlayerShelter()
    assert shelter.name == ''
    assert not shelter.defeated
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 0
    assert len(shelter.survivors) == 0
    assert type(shelter.zombies) is list
    assert type(shelter.supplies) is list
    assert type(shelter.obstacles) is list
    assert type(shelter.survivors) is list


def test_gui_default(fast_zombie, zombie, big_zombie):
    gs = GameState()
    gs.players = [PlayerShelter('Name_1'), PlayerShelter('Name_2'), PlayerShelter('Name_3')]
    gs.players[1].zombies = [zombie, fast_zombie, fast_zombie, big_zombie, zombie]
    gs.players[1].obstacles = [Supply.BARRICADES, Supply.ALARM]
    gs.players[1].survivors = [CityCard(), CityCard()]
    gs.players[2].zombies = [big_zombie, big_zombie]
    gs.players[2].obstacles = [Supply.MINE_FILED]
    gs.players[2].survivors = [CityCard(), CityCard(), CityCard()]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.zombies = [zombie]
    shelter.supplies = [Supply.AXE, Supply.MINE_FILED, Supply.LURE_OUT]
    shelter.obstacles = [Supply.MINE_FILED, Supply.ALARM]
    shelter.survivors = [CityCard(), CityCard(), CityCard(), CityCard()]
    shelter.gui_default(gs)
    assert len(tests.common.outputs) == 1
    assert len(tests.common.outputs[0]) == 582

    gs.city_deck = [zombie, CityCard()]
    shelter.gui_default(gs)
    assert len(tests.common.outputs) == 2
    assert len(tests.common.outputs[1]) == 604
