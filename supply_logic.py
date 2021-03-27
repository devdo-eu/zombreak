from zombie_enums import ZombieType
from supply_enums import Supply


def is_loud(supply):
    loud_supplies = [Supply.ALARM, Supply.MINE_FILED, Supply.MEGAPHONE, Supply.FLARE_GUN,
                     Supply.CHAINSAW, Supply.SWAP, Supply.SHOTGUN, Supply.GUN]
    return supply in loud_supplies


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
                    kill_zombie(shelter, supply, zombie_card, destroyed)
                    used = True
                elif not strong and zombie_card.top != ZombieType.BIG:
                    kill_zombie(shelter, supply, zombie_card, destroyed)
                    used = True
    if not used:
        shelter.print(f'Zombies inside shelter are too tough for an {weapon.value}!')


def kill_zombie(shelter, supply, zombie_card, destroyed):
    zombie = zombie_card.top
    shelter.print(f'One of survivors killed {zombie.value} with {supply.value}!')
    shelter.zombies.remove(zombie_card)
    if is_loud(supply):
        shelter.print('The sounds of the struggle could be heard from miles away!')
    if destroyed:
        shelter.print(f'{str(supply.value).capitalize()} has been destroyed!')
        shelter.supplies.remove(supply)


def play_axe(game_state):
    play_weapon(game_state, Supply.AXE)


def play_gun(game_state):
    play_weapon(game_state, Supply.GUN)


def play_shotgun(game_state):
    big_inside = False
    lesser_counter = 0
    shelter = game_state.active_player
    for zombie_card in shelter.zombies:
        if zombie_card.top == ZombieType.BIG:
            big_inside = True
        else:
            lesser_counter += 1

    if big_inside and lesser_counter == 0:
        play_weapon(game_state, Supply.SHOTGUN, strong=True)
    elif lesser_counter == 1 and not big_inside:
        play_weapon(game_state, Supply.SHOTGUN, destroyed=True)
    elif lesser_counter > 1 and not big_inside:
        play_weapon(game_state, Supply.SHOTGUN, destroyed=False)
        play_weapon(game_state, Supply.SHOTGUN)
    else:
        message = 'What survivors should do (0/1)?\n' \
                  '[0]: kill big zombie\n' \
                  f'[1]: kill up to two lesser zombies ({lesser_counter} inside)\n>>'
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            play_weapon(game_state, Supply.SHOTGUN, strong=True)
        elif lesser_counter == 1:
            play_weapon(game_state, Supply.SHOTGUN, destroyed=True)
        else:
            play_weapon(game_state, Supply.SHOTGUN, destroyed=False)
            play_weapon(game_state, Supply.SHOTGUN)


def get_action(game_state, message, possible_actions):
    shelter = game_state.active_player
    while True:
        action = shelter.input(message)
        if action in possible_actions:
            break
        else:
            shelter.print(f'No such action as {action}!')
    return action
