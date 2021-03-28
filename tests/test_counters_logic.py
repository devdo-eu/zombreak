from logic import PlayerShelter, CityCard
import counters_logic
from supply_enums import Supply
from tests.common import dumper_factory, helper_factory, gs, fast_zombie, zombie, big_zombie
import tests.common


def test_sanity_check():
    assert gs
    assert fast_zombie
    assert zombie
    assert big_zombie


def test_play_sacrifice(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[1]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0', '1', '0'])
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.survivors = [CityCard(), CityCard()]
    shelter.supplies = [Supply.SACRIFICE]
    counters_logic.play_sacrifice(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.players[0].zombies) == 2
    assert len(gs.players[2].zombies) == 1
    assert big_zombie in gs.players[2].zombies
    assert len(gs.city_graveyard) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_sacrifice_when_one_rivals_defeated(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.players[0].defeated = True
    gs.active_player = gs.players[1]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.survivors = [CityCard(), CityCard()]
    shelter.supplies = [Supply.SACRIFICE]
    counters_logic.play_sacrifice(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.players[0].zombies) == 0
    assert len(gs.players[2].zombies) == 3
    assert len(gs.city_graveyard) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_drone(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0', '1'])
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.DRONE]
    counters_logic.play_drone(gs)
    assert len(shelter.zombies) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_drone_only_big(gs, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.zombies = [big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.DRONE]
    counters_logic.play_drone(gs)
    assert len(shelter.zombies) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_drone_only_lesser_one_rival(gs, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    gs.players[1].defeated = True
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.zombies = [big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.DRONE]
    counters_logic.play_drone(gs)
    assert len(shelter.zombies) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_chainsaw(gs):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    gs.players[1].obstacles = [Supply.ALARM, Supply.BARRICADES, Supply.BARRICADES]
    gs.players[2].obstacles = [Supply.MINE_FILED]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.supplies = [Supply.CHAINSAW]
    counters_logic.play_chainsaw(gs)
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].obstacles) == 0
    assert len(gs.players[2].obstacles) == 1
    assert len(gs.supply_graveyard) == 4
    assert len(tests.common.outputs) == 3


def test_play_chainsaw_no_one_has_defence(gs):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.supplies = [Supply.CHAINSAW]
    counters_logic.play_chainsaw(gs)
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_takeover(gs):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.supplies = [Supply.TAKEOVER]
    gs.players[1].survivors = [CityCard()]
    gs.players[2].survivors = [CityCard()]
    counters_logic.play_takeover(gs)
    assert len(shelter.survivors) == 1
    assert len(gs.players[1].survivors) == 0
    assert gs.players[1].defeated
    assert len(gs.players[2].survivors) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(tests.common.outputs) == 2


def test_play_swap(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.supplies = [Supply.SWAP]
    shelter.zombies = [fast_zombie, big_zombie, fast_zombie, zombie]
    gs.players[1].obstacles = [Supply.BARRICADES, Supply.ALARM]
    counters_logic.play_swap(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.obstacles) == 2
    assert len(gs.players[1].zombies) == 4
    assert len(gs.players[1].obstacles) == 0
    assert len(tests.common.outputs) == 2


def test_play_lure_out(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['y', '1', '0', '0'])
    shelter.supplies = [Supply.LURE_OUT]
    shelter.zombies = [fast_zombie, big_zombie, fast_zombie, zombie]
    gs.city_deck = [zombie, CityCard()]
    counters_logic.play_lure_out(gs)
    assert len(shelter.zombies) == 3
    assert big_zombie not in shelter.zombies
    assert len(gs.players[1].zombies) == 1
    assert big_zombie in gs.players[1].zombies
    assert len(gs.players[2].zombies) == 1
    assert zombie in gs.players[2].zombies
    assert len(tests.common.outputs) == 2
