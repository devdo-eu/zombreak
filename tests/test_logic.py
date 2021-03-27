from logic import GameState, PlayerShelter, CityCard


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


def test_zombie_show_up():
    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.city_deck = [CityCard('zombie')]
    gs.zombie_show_up()
    assert gs.city_deck[0].top == 'zombie'
    assert gs.city_deck[0].bottom == 'survivor'
    assert len(gs.city_deck) == 1
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 1
    assert gs.active_player.zombies[0].top == 'zombie'
    assert len(gs.city_deck) == 0

    gs.city_deck = [CityCard('big zombie')]
    gs.zombie_show_up()
    assert gs.city_deck[0].top == 'big zombie'
    assert gs.city_deck[0].bottom == 'survivor'
    assert len(gs.city_deck) == 1
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 2
    assert gs.active_player.zombies[1].top == 'big zombie'
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
    gs.city_deck = [CityCard('fast zombie')]
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 1
    assert gs.active_player.zombies[0].top == 'fast zombie'
    assert len(gs.city_deck) == 0


def test_horde_show_up():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [CityCard('horde'), CityCard('zombie'), CityCard('zombie'), CityCard('zombie'),
                    CityCard('zombie'), CityCard('zombie'), CityCard('zombie'), CityCard('zombie')]
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
    gs.city_deck = [CityCard('horde'), CityCard('zombie'), CityCard('zombie')]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 0

    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    gs.active_player = gs.players[2]
    gs.city_deck = [CityCard('horde'), CityCard('zombie'), CityCard('zombie')]
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
    gs.city_deck = [CityCard('horde'), CityCard('zombie'), CityCard('zombie')]
    gs.city_graveyard = [CityCard('zombie'), CityCard('survivor'), CityCard('zombie')]
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
    gs.city_deck = [CityCard('horde'), CityCard('zombie'), CityCard('horde'), CityCard('zombie'),
                    CityCard('zombie'), CityCard('zombie'), CityCard('zombie'), CityCard('zombie')]
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
    gs.city_deck = [CityCard('horde'), CityCard('horde'), CityCard('zombie'), CityCard('zombie'),
                    CityCard('zombie'), CityCard('zombie'), CityCard('zombie'), CityCard('zombie')]
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
    gs.supply_deck = ['axe', 'alarm', 'axe', 'gun']
    gs.get_supplies()
    assert len(gs.supply_deck) == 1
    assert gs.supply_deck[0] == 'gun'
    assert len(gs.active_player.supplies) == 3

    gs = GameState()
    gs.active_player = PlayerShelter()
    gs.supply_deck = ['axe', 'alarm', 'axe', 'gun']
    gs.active_player.supplies = ['radio', 'drone']
    gs.get_supplies()
    assert len(gs.supply_deck) == 3
    assert gs.supply_deck[0] == 'alarm'
    assert len(gs.active_player.supplies) == 3


def test_end_active_player_turn_no_zombies():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    for player in gs.players:
        player.survivors.append(CityCard('zombie'))
    gs.active_player = gs.players[2]
    gs.supply_deck = ['axe', 'alarm', 'axe', 'gun']
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 3


def test_end_active_player_turn_no_supplies_more_in_graveyard():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    for player in gs.players:
        player.survivors.append(CityCard('zombie'))
    gs.active_player = gs.players[2]
    gs.supply_deck = ['axe']
    gs.supply_graveyard = ['alarm', 'drone']
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 3
    assert len(gs.supply_graveyard) == 0


def test_end_active_player_turn_no_supplies():
    gs = GameState()
    gs.players = [PlayerShelter(), PlayerShelter(), PlayerShelter()]
    for player in gs.players:
        player.survivors.append(CityCard('zombie'))
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
    for player in gs.players:
        player.survivors.append(CityCard('zombie'))
    gs.active_player = gs.players[2]
    gs.active_player.supplies = ['axe', 'alarm']
    zombie_card = CityCard('zombie')
    zombie_card.flip()
    gs.active_player.zombies = [zombie_card]
    gs.supply_deck = ['axe', 'alarm', 'axe', 'gun']
    gs.end_active_player_turn()
    assert gs.active_player == gs.players[0]
    assert len(gs.players[2].supplies) == 0
