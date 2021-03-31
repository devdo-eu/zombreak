from logic.common import is_loud, put_supplies_on_graveyard
from enums.zombie import ZombieType
from enums.supply import Supply


def play_summon(game_state, summon):
    shelter = game_state.active_player
    arrives = 1
    if summon == Supply.FLARE_GUN:
        arrives = 2
    shelter.print(f'One of survivors used {summon.value}!')
    if is_loud(summon):
        shelter.print(f'The sounds of the {summon.value} could be heard from miles away!')
    for _ in range(arrives):
        if len(game_state.city_deck) > 0 and game_state.city_deck[0].top == ZombieType.SURVIVOR:
            card = game_state.get_city_card()
            shelter.print(f'New survivor has arrived to "{shelter.name}" shelter!')
            shelter.survivors.append(card)
        elif summon == Supply.RADIO:
            shelter.print(f'Survivors cannot use {summon.value} when zombies roam all over the city!')
            return
        else:
            shelter.print('Nobody else arrived...')
            break
    put_supplies_on_graveyard(game_state, summon)


def play_radio(game_state):
    play_summon(game_state, Supply.RADIO)


def play_megaphone(game_state):
    play_summon(game_state, Supply.MEGAPHONE)


def play_flare_gun(game_state):
    play_summon(game_state, Supply.FLARE_GUN)
