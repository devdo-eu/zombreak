from logic import PlayerShelter, CityCard, GameState
import supply_logic
import pytest
from zombie_enums import ZombieType
from supply_enums import Supply

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


def test_play_axe(gs, zombie, big_zombie, fast_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.AXE, Supply.AXE, Supply.AXE]
    supply_logic.play_axe(gs)
    assert len(shelter.supplies) == 2
    assert len(shelter.zombies) == 2
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert zombie not in shelter.zombies
    assert len(outputs) == 2

    supply_logic.play_axe(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(outputs) == 4

    supply_logic.play_axe(gs)
    assert len(shelter.supplies) == 0
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 3
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(outputs) == 6


def test_play_gun(gs, zombie, big_zombie, fast_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.GUN, Supply.GUN, Supply.GUN]
    supply_logic.play_gun(gs)
    assert len(shelter.supplies) == 2
    assert len(shelter.zombies) == 2
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert zombie not in shelter.zombies
    assert len(outputs) == 3

    supply_logic.play_gun(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(outputs) == 6

    supply_logic.play_gun(gs)
    assert len(shelter.supplies) == 0
    assert len(shelter.zombies) == 1
    assert len(gs.supply_graveyard) == 3
    assert len(gs.city_graveyard) == 2
    assert big_zombie in shelter.zombies
    assert len(outputs) == 8


def test_play_shotgun_one_big(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 3


def test_play_shotgun_many_big(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie, big_zombie, big_zombie, big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 5
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 3


def test_play_shotgun_one_lesser(gs, fast_zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 3


def test_play_shotgun_two_lesser(gs, fast_zombie, zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 2
    assert len(outputs) == 5


def test_play_shotgun_many_lesser(gs, fast_zombie, zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 4
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 2
    assert len(outputs) == 5


def test_play_shotgun_many_lesser_one_big(gs, fast_zombie, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 6
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 5
    assert big_zombie in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 3
    assert len(outputs) == 5


def test_play_shotgun_many_lesser_one_big_wrong_input(gs, fast_zombie, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['6', 'rgdfrbw', '0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 6
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 5


def test_play_sniper_rifle_on_city(gs, zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['y']))
    shelter = gs.active_player
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 1
    assert zombie not in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 3


def test_play_sniper_rifle_zombie_in_city_and_shelter(gs, zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['y']))
    shelter = gs.active_player
    shelter.zombies = [big_zombie, zombie]
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 1
    assert len(shelter.zombies) == 2
    assert zombie not in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['n', '0']))
    shelter = gs.active_player
    shelter.zombies = [big_zombie, zombie]
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 2
    assert len(shelter.zombies) == 1
    assert big_zombie not in shelter.zombies
    assert zombie in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert len(outputs) == 2


def test_play_sniper_rifle_big_zombies(gs, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [big_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 2


def test_play_sniper_rifle_lesser_zombies(gs, fast_zombie, zombie):
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 2


def test_play_sniper_rifle_lesser_and_big_zombies(gs, fast_zombie, big_zombie):
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 1
    assert len(outputs) == 2

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 2
    assert len(outputs) == 2


def test_play_radio(gs):
    shelter = gs.active_player
    gs.city_deck = [CityCard()]
    shelter.supplies = [Supply.RADIO]
    supply_logic.play_radio(gs)
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.supplies = [Supply.RADIO]
    supply_logic.play_radio(gs)
    assert len(shelter.survivors) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(outputs) == 3


def test_play_megaphone(gs):
    shelter = gs.active_player
    gs.city_deck = [CityCard()]
    shelter.supplies = [Supply.MEGAPHONE]
    supply_logic.play_megaphone(gs)
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 4

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    gs.city_deck = []
    shelter.supplies = [Supply.MEGAPHONE]
    supply_logic.play_megaphone(gs)
    assert len(shelter.survivors) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(outputs) == 4


def test_play_flare_gun(gs):
    shelter = gs.active_player
    gs.city_deck = [CityCard()]
    shelter.supplies = [Supply.FLARE_GUN]
    supply_logic.play_flare_gun(gs)
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    gs.city_deck = [CityCard(), CityCard()]
    shelter.supplies = [Supply.FLARE_GUN]
    supply_logic.play_flare_gun(gs)
    assert len(shelter.survivors) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    gs.city_deck = []
    shelter.supplies = [Supply.FLARE_GUN]
    supply_logic.play_flare_gun(gs)
    assert len(shelter.survivors) == 0
    assert len(shelter.supplies) == 0
    assert len(gs.city_deck) == 0
    assert len(gs.supply_graveyard) == 3
    assert len(outputs) == 4


def test_play_alarm(gs):
    shelter = gs.active_player
    shelter.supplies = [Supply.ALARM]
    supply_logic.play_alarm(gs)
    assert len(outputs) == 1
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 1
    assert len(gs.supply_graveyard) == 0
    for hungry_zombie in shelter.zombies:
        assert hungry_zombie.active


def test_defend_with_alarm(gs, fast_zombie, zombie, big_zombie):
    shelter = gs.active_player
    shelter.survivors = [CityCard()]
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.ALARM]
    supply_logic.defend_with_alarm(gs)
    assert len(outputs) == 4
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    for hungry_zombie in shelter.zombies:
        assert not hungry_zombie.active


def test_play_barricades(gs):
    shelter = gs.active_player
    shelter.supplies = [Supply.BARRICADES]
    supply_logic.play_barricades(gs)
    assert len(outputs) == 1
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 1
    assert len(gs.supply_graveyard) == 0
    for hungry_zombie in shelter.zombies:
        assert hungry_zombie.active


def test_defend_with_barricades(gs, fast_zombie, zombie, big_zombie):
    shelter = gs.active_player
    shelter.survivors = [CityCard()]
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.BARRICADES]
    supply_logic.defend_with_barricades(gs)
    assert len(outputs) == 3
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    number_of_stopped_zombies = 0
    for hungry_zombie in shelter.zombies:
        if not hungry_zombie.active:
            number_of_stopped_zombies += 1
    assert number_of_stopped_zombies == 1


def test_play_mine_field(gs):
    shelter = gs.active_player
    shelter.supplies = [Supply.MINE_FILED]
    supply_logic.play_mine_field(gs)
    assert len(outputs) == 1
    assert len(shelter.supplies) == 0
    assert len(shelter.obstacles) == 1
    assert len(gs.supply_graveyard) == 0
    for hungry_zombie in shelter.zombies:
        assert hungry_zombie.active


def test_defend_with_mine_field(gs, fast_zombie, zombie, big_zombie):
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    supply_logic.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(gs.city_graveyard) == 2
    assert len(outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    supply_logic.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie in shelter.zombies
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 2
    assert len(gs.city_graveyard) == 4
    assert len(outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory(),
                                     input_foo=helper_factory(['1', '1']))
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    supply_logic.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 1
    assert big_zombie in shelter.zombies
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 3
    assert len(gs.city_graveyard) == 6
    assert len(outputs) == 5

    gs.active_player = PlayerShelter(print_foo=dumper_factory(),
                                     input_foo=helper_factory(['1', '0']))
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.obstacles = [Supply.MINE_FILED]
    supply_logic.defend_with_mine_field(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie in shelter.zombies
    assert len(shelter.obstacles) == 0
    assert len(gs.supply_graveyard) == 4
    assert len(gs.city_graveyard) == 8
    assert len(outputs) == 5


def test_play_sacrifice(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[1]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0', '1', '0'])
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.survivors = [CityCard(), CityCard()]
    shelter.supplies = [Supply.SACRIFICE]
    supply_logic.play_sacrifice(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.players[0].zombies) == 2
    assert len(gs.players[2].zombies) == 1
    assert big_zombie in gs.players[2].zombies
    assert len(gs.city_graveyard) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_sacrifice_when_one_rivals_defeated(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.players[0].defeated = True
    gs.active_player = gs.players[1]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.survivors = [CityCard(), CityCard()]
    shelter.supplies = [Supply.SACRIFICE]
    supply_logic.play_sacrifice(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.survivors) == 1
    assert len(shelter.supplies) == 0
    assert len(gs.players[0].zombies) == 0
    assert len(gs.players[2].zombies) == 3
    assert len(gs.city_graveyard) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_drone(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0', '1'])
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.DRONE]
    supply_logic.play_drone(gs)
    assert len(shelter.zombies) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_drone_only_big(gs, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.zombies = [big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.DRONE]
    supply_logic.play_drone(gs)
    assert len(shelter.zombies) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_drone_only_lesser_one_rival(gs, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    gs.players[1].defeated = True
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.zombies = [big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.DRONE]
    supply_logic.play_drone(gs)
    assert len(shelter.zombies) == 2
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_chainsaw(gs):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    gs.players[1].obstacles = [Supply.ALARM, Supply.BARRICADES, Supply.BARRICADES]
    gs.players[2].obstacles = [Supply.MINE_FILED]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.supplies = [Supply.CHAINSAW]
    supply_logic.play_chainsaw(gs)
    assert len(shelter.supplies) == 0
    assert len(gs.players[1].obstacles) == 0
    assert len(gs.players[2].obstacles) == 1
    assert len(gs.supply_graveyard) == 4
    assert len(outputs) == 3


def test_play_chainsaw_no_one_has_defence(gs):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.supplies = [Supply.CHAINSAW]
    supply_logic.play_chainsaw(gs)
    assert len(shelter.supplies) == 0
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_takeover(gs):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.supplies = [Supply.TAKEOVER]
    gs.players[1].survivors = [CityCard()]
    gs.players[2].survivors = [CityCard()]
    supply_logic.play_takeover(gs)
    assert len(shelter.survivors) == 1
    assert len(gs.players[1].survivors) == 0
    assert gs.players[1].defeated
    assert len(gs.players[2].survivors) == 1
    assert len(gs.supply_graveyard) == 1
    assert len(outputs) == 2


def test_play_swap(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['0'])
    shelter.supplies = [Supply.SWAP]
    shelter.zombies = [fast_zombie, big_zombie, fast_zombie, zombie]
    gs.players[1].obstacles = [Supply.BARRICADES, Supply.ALARM]
    supply_logic.play_swap(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.obstacles) == 2
    assert len(gs.players[1].zombies) == 4
    assert len(gs.players[1].obstacles) == 0
    assert len(outputs) == 2


def test_play_lure_out(gs, fast_zombie, zombie, big_zombie):
    gs.players = [PlayerShelter('ZERO'), PlayerShelter('FIRST'), PlayerShelter('SECOND')]
    gs.active_player = gs.players[0]
    shelter = gs.active_player
    shelter.print = dumper_factory()
    shelter.input = helper_factory(['y', '1', '0', '0'])
    shelter.supplies = [Supply.LURE_OUT]
    shelter.zombies = [fast_zombie, big_zombie, fast_zombie, zombie]
    gs.city_deck = [zombie, CityCard()]
    supply_logic.play_lure_out(gs)
    assert len(shelter.zombies) == 3
    assert big_zombie not in shelter.zombies
    assert len(gs.players[1].zombies) == 1
    assert big_zombie in gs.players[1].zombies
    assert len(gs.players[2].zombies) == 1
    assert zombie in gs.players[2].zombies
    assert len(outputs) == 2
