from logic import PlayerShelter, CityCard, GameState
import supply_logic
from zombie_enums import ZombieType
from supply_enums import Supply

outputs = []
helper_move = [-1, -1]
zombie = CityCard(ZombieType.ZOMBIE)
zombie.flip()
big_zombie = CityCard(ZombieType.BIG)
big_zombie.flip()
fast_zombie = CityCard(ZombieType.FAST)
fast_zombie.flip()


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


def test_play_axe():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.AXE, Supply.AXE, Supply.AXE]
    supply_logic.play_axe(gs)
    assert len(shelter.supplies) == 2
    assert len(shelter.zombies) == 2
    assert zombie not in shelter.zombies
    assert len(outputs) == 2

    supply_logic.play_axe(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert big_zombie in shelter.zombies
    assert len(outputs) == 4

    supply_logic.play_axe(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert big_zombie in shelter.zombies
    assert len(outputs) == 5


def test_play_gun():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [zombie, big_zombie, fast_zombie]
    shelter.supplies = [Supply.GUN, Supply.GUN, Supply.GUN]
    supply_logic.play_gun(gs)
    assert len(shelter.supplies) == 2
    assert len(shelter.zombies) == 2
    assert zombie not in shelter.zombies
    assert len(outputs) == 3

    supply_logic.play_gun(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert big_zombie in shelter.zombies
    assert len(outputs) == 6

    supply_logic.play_gun(gs)
    assert len(shelter.supplies) == 1
    assert len(shelter.zombies) == 1
    assert big_zombie in shelter.zombies
    assert len(outputs) == 7


def test_play_shotgun_one_big():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [big_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(outputs) == 3


def test_play_shotgun_many_big():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [big_zombie, big_zombie, big_zombie, big_zombie, big_zombie, big_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 5
    assert len(shelter.supplies) == 0
    assert len(outputs) == 3


def test_play_shotgun_one_lesser():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [fast_zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(outputs) == 3


def test_play_shotgun_two_lesser():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(outputs) == 5


def test_play_shotgun_many_lesser():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 4
    assert len(shelter.supplies) == 0
    assert len(outputs) == 5


def test_play_shotgun_many_lesser_one_big():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 6
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(outputs) == 3

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 5
    assert big_zombie in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(outputs) == 5


def test_play_shotgun_many_lesser_one_big_wrong_input():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['6', 'rgdfrbw', '0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie, fast_zombie, big_zombie, fast_zombie, zombie, zombie]
    shelter.supplies = [Supply.SHOTGUN]
    supply_logic.play_shotgun(gs)
    assert len(shelter.zombies) == 6
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(outputs) == 5


def test_play_sniper_rifle_on_city():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['y']))
    shelter = gs.active_player
    gs.city_deck = [zombie, CityCard()]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(gs.city_deck) == 1
    assert zombie not in gs.city_deck
    assert len(shelter.supplies) == 0
    assert len(outputs) == 3


def test_play_sniper_rifle_zombie_in_city_and_shelter():
    gs = GameState()
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
    assert len(outputs) == 2


def test_play_sniper_rifle_big_zombies():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [big_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert len(shelter.supplies) == 0
    assert len(outputs) == 2


def test_play_sniper_rifle_lesser_zombies():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory())
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert len(shelter.supplies) == 0
    assert len(outputs) == 2


def test_play_sniper_rifle_lesser_and_big_zombies():
    gs = GameState()
    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['0']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert big_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(outputs) == 2

    gs.active_player = PlayerShelter(print_foo=dumper_factory(), input_foo=helper_factory(['1']))
    shelter = gs.active_player
    shelter.zombies = [fast_zombie, big_zombie]
    shelter.supplies = [Supply.SNIPER]
    supply_logic.play_sniper_rifle(gs)
    assert len(shelter.zombies) == 1
    assert fast_zombie not in shelter.zombies
    assert len(shelter.supplies) == 0
    assert len(outputs) == 2
