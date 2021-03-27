from logic import GameState, PlayerShelter, CityCard
from zombie_enums import ZombieType
from supply_enums import Supply


def test_game_state_ctor():
    gs = GameState()
    assert not gs.finished
    assert type(gs.city_deck) is list
    assert type(gs.supply_deck) is list
    assert type(gs.city_graveyard) is list
    assert type(gs.supply_graveyard) is list
    assert type(gs.players) is list
    assert gs.active_player is None


def test_prepare_city_deck():
    gs = GameState()
    gs.prepare_city_deck()
    assert len(gs.city_deck) == 55


def test_prepare_supply_deck():
    gs = GameState()
    gs.prepare_supply_deck()
    assert len(gs.supply_deck) == 55


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


def test_city_card_ctor_exception():
    thrown = False
    try:
        _survivor = CityCard(ZombieType.SURVIVOR)
    except Exception as ex:
        assert str(ex) == 'Card cannot be init with survivor on top!'
        thrown = True
    assert thrown


def test_zombie_show_up():
    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.city_deck = [CityCard(ZombieType.ZOMBIE)]
    gs.zombie_show_up()
    assert gs.city_deck[0].top == ZombieType.ZOMBIE
    assert gs.city_deck[0].bottom == ZombieType.SURVIVOR
    assert len(gs.city_deck) == 1
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 1
    assert gs.active_player.zombies[0].top == ZombieType.ZOMBIE
    assert len(gs.city_deck) == 0

    gs.city_deck = [CityCard(ZombieType.BIG)]
    gs.zombie_show_up()
    assert gs.city_deck[0].top == ZombieType.BIG
    assert gs.city_deck[0].bottom == ZombieType.SURVIVOR
    assert len(gs.city_deck) == 1
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 2
    assert gs.active_player.zombies[1].top == ZombieType.BIG
    assert len(gs.city_deck) == 0


def test_zombie_show_up_empty_city():
    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.city_deck = []
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 0


def test_fast_zombie_show_up():
    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.city_deck = [CityCard(ZombieType.FAST)]
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 1
    assert gs.active_player.zombies[0].top == ZombieType.FAST
    assert len(gs.city_deck) == 0


def test_horde_show_up():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[1]
    horde = ZombieType.HORDE
    zombie = ZombieType.ZOMBIE
    gs.city_deck = [CityCard(horde), CityCard(zombie), CityCard(zombie), CityCard(zombie),
                    CityCard(zombie), CityCard(zombie), CityCard(zombie), CityCard(zombie)]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 4
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 1


def test_horde_show_up_two_zombies_left_in_city_no_graveyard():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [CityCard(ZombieType.HORDE), CityCard(ZombieType.ZOMBIE), CityCard(ZombieType.ZOMBIE)]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 0

    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[2]
    gs.city_deck = [CityCard(ZombieType.HORDE), CityCard(ZombieType.ZOMBIE), CityCard(ZombieType.ZOMBIE)]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 0
    assert len(gs.active_player.zombies) == 0


def test_horde_show_up_two_zombies_left_in_city_more_on_graveyard():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [CityCard(ZombieType.HORDE), CityCard(ZombieType.ZOMBIE), CityCard(ZombieType.ZOMBIE)]
    survivor_card = CityCard(ZombieType.ZOMBIE)
    survivor_card.flip()
    gs.city_graveyard = [CityCard(ZombieType.ZOMBIE), survivor_card, CityCard(ZombieType.ZOMBIE)]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 2
    assert len(gs.city_graveyard) == 1
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 1


def test_horde_show_up_second_time():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[1]
    horde = ZombieType.HORDE
    zombie = ZombieType.ZOMBIE
    gs.city_deck = [CityCard(horde), CityCard(zombie), CityCard(horde), CityCard(zombie),
                    CityCard(zombie), CityCard(zombie), CityCard(zombie), CityCard(zombie)]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.city_graveyard) == 2
    assert len(gs.players[0].zombies) == 2
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 2
    assert len(gs.active_player.zombies) == 1

    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[2]
    gs.city_deck = [CityCard(horde), CityCard(horde), CityCard(zombie), CityCard(zombie),
                    CityCard(zombie), CityCard(zombie), CityCard(zombie), CityCard(zombie)]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.city_graveyard) == 2
    assert len(gs.players[0].zombies) == 2
    assert len(gs.players[1].zombies) == 2
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 1


def test_get_supplies():
    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.supply_deck = [Supply.AXE, Supply.ALARM, Supply.AXE, Supply.GUN]
    gs.get_supplies()
    assert len(gs.supply_deck) == 1
    assert gs.supply_deck[0] == Supply.GUN
    assert len(gs.active_player.supplies) == 3

    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.supply_deck = [Supply.AXE, Supply.ALARM, Supply.AXE, Supply.GUN]
    gs.active_player.supplies = [Supply.RADIO, Supply.DRONE]
    gs.get_supplies()
    assert len(gs.supply_deck) == 3
    assert gs.supply_deck[0] == Supply.ALARM
    assert len(gs.active_player.supplies) == 3


def test_end_active_player_turn_no_zombies():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    survivor_card = CityCard(ZombieType.ZOMBIE)
    survivor_card.flip()
    for player in gs.players:
        player.survivors.append(survivor_card)
    gs.active_player = gs.players[2]
    gs.supply_deck = [Supply.AXE, Supply.ALARM, Supply.AXE, Supply.GUN]
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 3


def test_end_active_player_turn_no_supplies_more_in_graveyard():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    survivor_card = CityCard(ZombieType.ZOMBIE)
    survivor_card.flip()
    for player in gs.players:
        player.survivors.append(survivor_card)
    gs.active_player = gs.players[2]
    gs.supply_deck = [Supply.AXE]
    gs.supply_graveyard = [Supply.ALARM, Supply.DRONE]
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 3
    assert len(gs.supply_graveyard) == 0


def test_end_active_player_turn_no_supplies():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    survivor_card = CityCard(ZombieType.ZOMBIE)
    survivor_card.flip()
    for player in gs.players:
        player.survivors.append(survivor_card)
    gs.active_player = gs.players[2]
    gs.supply_deck = []
    gs.supply_graveyard = []
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 0
    assert len(gs.supply_graveyard) == 0


def test_end_active_player_turn_zombies_no_obstacles():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    survivor_card = CityCard(ZombieType.ZOMBIE)
    survivor_card.flip()
    for player in gs.players:
        player.survivors.append(survivor_card)
    gs.active_player = gs.players[2]
    gs.active_player.supplies = [Supply.AXE, Supply.ALARM]
    zombie_card = CityCard(ZombieType.ZOMBIE)
    zombie_card.flip()
    gs.active_player.zombies = [zombie_card]
    gs.supply_deck = [Supply.AXE, Supply.ALARM, Supply.AXE, Supply.GUN]
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 0
