from zombie_enums import ZombieType
from supply_enums import Supply


def is_loud(supply):
    loud_supplies = [Supply.ALARM, Supply.MINE_FILED, Supply.MEGAPHONE, Supply.FLARE_GUN,
                     Supply.CHAINSAW, Supply.SWAP, Supply.SHOTGUN, Supply.GUN]
    return supply in loud_supplies


def put_supplies_on_graveyard(game_state, supply, obstacle=False):
    shelter = game_state.active_player
    shelter.print(f'{str(supply.value).capitalize()} has been destroyed!')
    if not obstacle:
        shelter.supplies.remove(supply)
    else:
        shelter.obstacles.remove(supply)
    game_state.supply_graveyard.append(supply)


def put_zombie_on_graveyard(game_state, zombie_card):
    shelter = game_state.active_player
    shelter.zombies.remove(zombie_card)
    game_state.city_graveyard.append(zombie_card)


def get_action(game_state, message, possible_actions):
    shelter = game_state.active_player
    if len(possible_actions) == 1:
        return possible_actions[0]
    while True:
        action = shelter.input(message)
        if action in possible_actions:
            break
        else:
            shelter.print(f'No such action as {action}!')
    return action


def find_rivals_and_build_action_message(game_state):
    shelter = game_state.active_player
    rivals = []
    choice_message = ''
    possible_actions = []
    for rival in game_state.players:
        if rival != shelter and not rival.defeated:
            rivals.append(rival)
    for index, rival in enumerate(rivals):
        choice_message += f'[{index}]: {rival.name} shelter\n'
        possible_actions.append(str(index))
    return choice_message, possible_actions, rivals


def count_zombies(game_state):
    shelter = game_state.active_player
    big_inside = False
    lesser_counter = 0
    for zombie_card in shelter.zombies:
        if zombie_card.top == ZombieType.BIG:
            big_inside = True
        else:
            lesser_counter += 1
    return big_inside, lesser_counter


def count_zombies_and_execute_function(game_state, message, execute, count=2):
    shelter = game_state.active_player
    big_inside, lesser_counter = count_zombies(game_state)
    if len(shelter.zombies) < count or (big_inside and lesser_counter == 0) or not big_inside:
        zombie_card = shelter.zombies[0]
        execute(zombie_card)
    else:
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            zombie_type = [ZombieType.BIG]
        else:
            zombie_type = [ZombieType.FAST, ZombieType.ZOMBIE]
        for zombie in shelter.zombies:
            if zombie.top in zombie_type:
                zombie_card = zombie
                execute(zombie_card)
                break
