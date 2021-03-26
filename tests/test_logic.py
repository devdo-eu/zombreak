import logic


def test_game_state_ctor():
    gs = logic.GameState()
    assert type(gs.city_deck) is list
    assert type(gs.supply_deck) is list
    assert type(gs.city_graveyard) is list
    assert type(gs.supply_graveyard) is list
    assert type(gs.players) is list
    assert gs.active_player is None


def test_prepare_city_deck():
    gs = logic.GameState()
    gs.prepare_city_deck()
    assert len(gs.city_deck) == 55


def test_prepare_supply_deck():
    gs = logic.GameState()
    gs.prepare_supply_deck()
    assert len(gs.supply_deck) == 55


def test_player_shelter_class():
    shelter = logic.PlayerShelter()
    assert shelter.name == ''
    assert len(shelter.zombies) == 0
    assert len(shelter.supplies) == 0
    assert len(shelter.survivors) == 0
    assert type(shelter.zombies) is list
    assert type(shelter.supplies) is list
    assert type(shelter.survivors) is list


def test_zombie_show_up():
    gs = logic.GameState()
    gs.active_player = logic.PlayerShelter()
    gs.city_deck = [['survivor', 'zombie']]
    gs.zombie_show_up()
    assert gs.city_deck[0][0] == 'zombie'
    assert gs.city_deck[0][1] == 'survivor'
    assert len(gs.city_deck) == 1
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 1
    assert gs.active_player.zombies[0] == 'zombie'
    assert len(gs.city_deck) == 0

    gs.city_deck = [['survivor', 'big zombie']]
    gs.zombie_show_up()
    assert gs.city_deck[0][0] == 'big zombie'
    assert gs.city_deck[0][1] == 'survivor'
    assert len(gs.city_deck) == 1
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 2
    assert gs.active_player.zombies[1] == 'big zombie'
    assert len(gs.city_deck) == 0


def test_zombie_show_up_empty_city():
    gs = logic.GameState()
    gs.active_player = logic.PlayerShelter()
    gs.city_deck = []
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 0


def test_fast_zombie_show_up():
    gs = logic.GameState()
    gs.active_player = logic.PlayerShelter()
    gs.city_deck = [['survivor', 'fast zombie']]
    gs.zombie_show_up()
    assert len(gs.active_player.zombies) == 1
    assert gs.active_player.zombies[0] == 'fast zombie'
    assert len(gs.city_deck) == 0


def test_horde_show_up():
    gs = logic.GameState()
    gs.players = [logic.PlayerShelter(), logic.PlayerShelter(), logic.PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [['survivor', 'horde'], ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie'],
                    ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 4
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 1


def test_horde_show_up_two_zombies_left_in_city_no_graveyard():
    gs = logic.GameState()
    gs.players = [logic.PlayerShelter(), logic.PlayerShelter(), logic.PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [['survivor', 'horde'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 0
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 0

    gs = logic.GameState()
    gs.players = [logic.PlayerShelter(), logic.PlayerShelter(), logic.PlayerShelter()]
    gs.active_player = gs.players[2]
    gs.city_deck = [['survivor', 'horde'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 0
    assert len(gs.active_player.zombies) == 0


def test_horde_show_up_two_zombies_left_in_city_more_on_graveyard():
    gs = logic.GameState()
    gs.players = [logic.PlayerShelter(), logic.PlayerShelter(), logic.PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [['survivor', 'horde'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.city_graveyard = [['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 2
    assert len(gs.city_graveyard) == 1
    assert len(gs.players[0].zombies) == 1
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 1


def test_horde_show_up_second_time():
    gs = logic.GameState()
    gs.players = [logic.PlayerShelter(), logic.PlayerShelter(), logic.PlayerShelter()]
    gs.active_player = gs.players[1]
    gs.city_deck = [['survivor', 'horde'], ['survivor', 'zombie'], ['survivor', 'horde'], ['survivor', 'zombie'],
                    ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.city_graveyard) == 2
    assert len(gs.players[0].zombies) == 2
    assert len(gs.players[1].zombies) == 1
    assert len(gs.players[2].zombies) == 2
    assert len(gs.active_player.zombies) == 1

    gs = logic.GameState()
    gs.players = [logic.PlayerShelter(), logic.PlayerShelter(), logic.PlayerShelter()]
    gs.active_player = gs.players[2]
    gs.city_deck = [['survivor', 'horde'], ['survivor', 'horde'], ['survivor', 'zombie'], ['survivor', 'zombie'],
                    ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie'], ['survivor', 'zombie']]
    gs.zombie_show_up()
    assert len(gs.city_deck) == 0
    assert len(gs.city_graveyard) == 2
    assert len(gs.players[0].zombies) == 2
    assert len(gs.players[1].zombies) == 2
    assert len(gs.players[2].zombies) == 1
    assert len(gs.active_player.zombies) == 1
