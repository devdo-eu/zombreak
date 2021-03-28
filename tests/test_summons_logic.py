from logic import PlayerShelter, CityCard
from supply_enums import Supply
import summons_logic
from tests.common import dumper_factory, gs, fast_zombie, zombie, big_zombie
import tests.common


def test_sanity_check():
    assert gs
    assert fast_zombie
    assert zombie
    assert big_zombie


def test_play_radio(gs):
    shelter = gs.active_player
    gs.city_deck = [CityCard()]
    shelter.supplies = [Supply.RADIO]
    summons_logic.play_radio(gs)
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.supplies = [Supply.RADIO]
    summons_logic.play_radio(gs)
    assert len(shelter.survivors) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(tests.common.outputs) == 3


def test_play_megaphone(gs):
    shelter = gs.active_player
    gs.city_deck = [CityCard()]
    shelter.supplies = [Supply.MEGAPHONE]
    summons_logic.play_megaphone(gs)
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 4

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    gs.city_deck = []
    shelter.supplies = [Supply.MEGAPHONE]
    summons_logic.play_megaphone(gs)
    assert len(shelter.survivors) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(tests.common.outputs) == 4


def test_play_flare_gun(gs):
    shelter = gs.active_player
    gs.city_deck = [CityCard()]
    shelter.supplies = [Supply.FLARE_GUN]
    summons_logic.play_flare_gun(gs)
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    gs.city_deck = [CityCard(), CityCard()]
    shelter.supplies = [Supply.FLARE_GUN]
    summons_logic.play_flare_gun(gs)
    assert len(shelter.survivors) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(tests.common.outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    gs.city_deck = []
    shelter.supplies = [Supply.FLARE_GUN]
    summons_logic.play_flare_gun(gs)
    assert len(shelter.survivors) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 3
    assert len(tests.common.outputs) == 4
