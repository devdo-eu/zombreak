from zombie_enums import ZombieType
from supply_enums import Supply
from common_logic import put_zombie_on_graveyard, put_supplies_on_graveyard, is_loud, count_zombies, get_action


def play_weapon(game_state, weapon, strong=False, destroyed=True):
    shelter = game_state.active_player
    used = False
    for supply in shelter.supplies:
        if supply is weapon and not used:
            for zombie_card in shelter.zombies:
                if used:
                    break
                elif strong and zombie_card.top == ZombieType.BIG:
                    destroyed = True
                    kill_zombie(game_state, supply, zombie_card, destroyed)
                    used = True
                elif not strong and zombie_card.top != ZombieType.BIG:
                    kill_zombie(game_state, supply, zombie_card, destroyed)
                    used = True
    if not used:
        shelter.print(f'One of survivors used {weapon.value} for nothing!')
        put_supplies_on_graveyard(game_state, weapon)


def kill_zombie(game_state, supply, zombie_card, destroyed):
    shelter = game_state.active_player
    zombie = zombie_card.top
    shelter.print(f'One of survivors killed {zombie.value} with {supply.value}!')
    put_zombie_on_graveyard(game_state, zombie_card)
    if is_loud(supply):
        shelter.print('The sounds of the struggle could be heard from miles away!')
    if destroyed:
        put_supplies_on_graveyard(game_state, supply)


def play_axe(game_state):
    if len(game_state.active_player.zombies) > 0:
        play_weapon(game_state, Supply.AXE)
    else:
        game_state.active_player.print(f'You cannot play {Supply.AXE.value} for nothing!')


def play_gun(game_state):
    play_weapon(game_state, Supply.GUN)


def play_shotgun(game_state):
    big_inside, lesser_counter = count_zombies(game_state)
    if big_inside and lesser_counter == 0:
        play_weapon(game_state, Supply.SHOTGUN, strong=True)
    elif lesser_counter <= 1 and not big_inside:
        play_weapon(game_state, Supply.SHOTGUN)
    elif lesser_counter > 1 and not big_inside:
        play_weapon(game_state, Supply.SHOTGUN, destroyed=False)
        play_weapon(game_state, Supply.SHOTGUN)
    else:
        message = 'What survivors should do [0/1]?\n[0]: kill big zombie\n' \
                  f'[1]: kill up to two lesser zombies ({lesser_counter} inside)\n>'
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            play_weapon(game_state, Supply.SHOTGUN, strong=True)
        elif lesser_counter == 1:
            play_weapon(game_state, Supply.SHOTGUN)
        else:
            play_weapon(game_state, Supply.SHOTGUN, destroyed=False)
            play_weapon(game_state, Supply.SHOTGUN)


def play_sniper_rifle(game_state):
    shelter = game_state.active_player
    if len(game_state.city_deck) > 0:
        top_card = game_state.city_deck[0]
        if top_card.top != ZombieType.SURVIVOR:
            message = f'There is {top_card.top.value} in the city. Should the survivors shoot it[y/n]?\n>'
            action = get_action(game_state, message, ['y', 'n'])
            if action == 'y':
                shelter.print(f'One of survivors killed {top_card.top.value} with {Supply.SNIPER.value}!')
                shelter.print('City is safe now!')
                game_state.city_graveyard.append(game_state.get_city_card())
                put_supplies_on_graveyard(game_state, Supply.SNIPER)
                return

    big_inside, lesser_counter = count_zombies(game_state)

    if big_inside and lesser_counter == 0:
        play_weapon(game_state, Supply.SNIPER, strong=True)
    elif lesser_counter >= 0 and not big_inside:
        play_weapon(game_state, Supply.SNIPER)
    else:
        message = 'What survivors should do[0/1]?\n[0]: kill big zombie\n[1]: kill lesser zombie\n>'
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            play_weapon(game_state, Supply.SNIPER, strong=True)
        else:
            play_weapon(game_state, Supply.SNIPER)
