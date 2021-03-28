from city_card import CityCard
from player_shelter import PlayerShelter
from tests.common import dumper_factory, helper_factory, gs, fast_zombie, zombie, big_zombie
from supply_enums import Supply
import weapons_logic
import tests.common


def test_sanity_check():
    assert gs
    assert fast_zombie
    assert zombie
    assert big_zombie


def test_play_axe(gs, zombie, big_zombie, fast_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.AXE, Supply.AXE, Supply.AXE]
    weapons_logic.play_axe(gs)
    assert len(shelter.supplies) == 2
    assert len(shelter.zombies) == 2
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert zombie not in shelter.zombies
    assert len(tests.common.outputs) == 2

    weapons_logic.play_axe(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(tests.common.outputs) == 4

    weapons_logic.play_axe(gs)
    assert len(shelter.supplies) == 0
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 3
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(tests.common.outputs) == 6


def test_play_gun(gs, zombie, big_zombie, fast_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.GUN, Supply.GUN, Supply.GUN]
    weapons_logic.play_gun(gs)
    assert len(shelter.supplies) == 2
    assert len(shelter.zombies) == 2
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert zombie not in shelter.zombies
    assert len(tests.common.outputs) == 3

    weapons_logic.play_gun(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(tests.common.outputs) == 6

    weapons_logic.play_gun(gs)
    assert len(shelter.supplies) == 0
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 3
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(tests.common.outputs) == 8


def test_play_shotgun_one_big(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3


def test_play_shotgun_many_big(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie, big_zombie, big_zombie, big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 5
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3


def test_play_shotgun_one_lesser(gs, fast_zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3


def test_play_shotgun_two_lesser(gs, fast_zombie, zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 2
    assert len(tests.common.outputs) == 5


def test_play_shotgun_many_lesser(gs, fast_zombie, zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 4
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 2
    assert len(tests.common.outputs) == 5


def test_play_shotgun_one_lesser_one_big(gs, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [big_zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 1
    assert zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3


def test_play_shotgun_many_lesser_one_big(gs, fast_zombie, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 6
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 5
    assert big_zombie in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 3
    assert len(tests.common.outputs) == 5


def test_play_shotgun_many_lesser_one_big_wrong_input(gs, fast_zombie, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['6', 'rgdfrbw', '0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    weapons_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 6
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 5


def test_play_sniper_rifle_on_city(gs, zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['y']))
    shelter = gs.active_player
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 1
    assert zombie not in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3


def test_play_sniper_rifle_zombie_in_city_and_shelter(gs, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['y']))
    shelter = gs.active_player
    shelter.zombies = [big_zombie, zombie]
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 1
    assert len(shelter.zombies) == 2
    assert zombie not in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['n', '0']))
    shelter = gs.active_player
    shelter.zombies = [big_zombie, zombie]
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 2
    assert len(shelter.zombies) == 1
    assert big_zombie not in shelter.zombies
    assert zombie in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert len(tests.common.outputs) == 2


def test_play_sniper_rifle_big_zombies(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_sniper_rifle_lesser_zombies(gs, fast_zombie, zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_sniper_rifle_lesser_and_big_zombies(gs, fast_zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(tests.common.outputs) == 2

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    weapons_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert len(tests.common.outputs) == 2
