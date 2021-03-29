from city_card import CityCard
from player_shelter import PlayerShelter
from supply_enums import Supply
import defences
import pytest
from tests.common import dumper_factory, helper_factory, gs, fast_zombie, zombie, big_zombie
import tests.common


def test_sanity_check():
    assert gs
    assert fast_zombie
    assert zombie
    assert big_zombie


@pytest.fixture
def shelter(gs, fast_zombie, zombie, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    return shelter


def test_play_alarm(gs, shelter):
    shelter.supplies = [Supply.ALARM]
    defences.play_alarm(gs)
    assert len(tests.common.outputs) == 1
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 1
    assert len(gs.supply_graveyard) == 0
    for hungry_zombie in shelter.zombies:
        assert hungry_zombie.active


def test_defend_with_alarm(gs, shelter):
    shelter.survivors = [CityCard()]
    shelter.obstacles = [Supply.ALARM]
    defences.defend_with_alarm(gs)
    assert len(tests.common.outputs) == 4
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    for hungry_zombie in shelter.zombies:
        assert not hungry_zombie.active


def test_play_barricades(gs, shelter):
    shelter.supplies = [Supply.BARRICADES]
    defences.play_barricades(gs)
    assert len(tests.common.outputs) == 1
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 1
    assert len(gs.supply_graveyard) == 0
    for hungry_zombie in shelter.zombies:
        assert hungry_zombie.active


def test_defend_with_barricades(gs, shelter):
    shelter.survivors = [CityCard()]
    shelter.obstacles = [Supply.BARRICADES]
    defences.defend_with_barricades(gs)
    assert len(tests.common.outputs) == 3
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    number_of_stopped_zombies = 0
    for hungry_zombie in shelter.zombies:
        if not hungry_zombie.active:
            number_of_stopped_zombies += 1
    assert number_of_stopped_zombies == 1


def test_play_mine_field(gs, shelter):
    shelter.supplies = [Supply.MINE_FILED]
    defences.play_mine_field(gs)
    assert len(tests.common.outputs) == 1
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 1
    assert len(gs.supply_graveyard) == 0
    for hungry_zombie in shelter.zombies:
        assert hungry_zombie.active


def test_defend_with_mine_field(gs, fast_zombie, zombie, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    defences.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 2
    assert len(tests.common.outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    defences.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie in shelter.zombies
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 4
    assert len(tests.common.outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory(),
                                     input_foo=helper_factory(['1', '1']))
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    defences.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 1
    assert big_zombie in shelter.zombies
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 3
    assert len(gs.city_graveyard) == 6
    assert len(tests.common.outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory(),
                                     input_foo=helper_factory(['1', '0']))
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    defences.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie in shelter.zombies
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 4
    assert len(gs.city_graveyard) == 8
    assert len(tests.common.outputs) == 5


def test_defend_with_mine_field_one_zombie(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    defences.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3
