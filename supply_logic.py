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
    play_weapon(game_state, Supply.AXE)


def play_gun(game_state):
    play_weapon(game_state, Supply.GUN)


def play_shotgun(game_state):
    big_inside, lesser_counter = count_zombies(game_state)
    if big_inside and lesser_counter == 0:
        play_weapon(game_state, Supply.SHOTGUN, strong=True)
    elif lesser_counter == 1 and not big_inside:
        play_weapon(game_state, Supply.SHOTGUN)
    elif lesser_counter > 1 and not big_inside:
        play_weapon(game_state, Supply.SHOTGUN, destroyed=False)
        play_weapon(game_state, Supply.SHOTGUN)
    else:
        message = 'What survivors should do [0/1]?\n' \
                  '[0]: kill big zombie\n' \
                  f'[1]: kill up to two lesser zombies ({lesser_counter} inside)\n>>'
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            play_weapon(game_state, Supply.SHOTGUN, strong=True)
        elif lesser_counter == 1:
            play_weapon(game_state, Supply.SHOTGUN)
        else:
            play_weapon(game_state, Supply.SHOTGUN, destroyed=False)
            play_weapon(game_state, Supply.SHOTGUN)


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


def play_sniper_rifle(game_state):
    shelter = game_state.active_player
    if len(game_state.city_deck) > 0:
        top_card = game_state.city_deck[0]
        if top_card.top != ZombieType.SURVIVOR:
            message = f'There is {top_card.top.value} in the city. Should the survivors shoot it[y/n]? '
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
    elif lesser_counter > 0 and not big_inside:
        play_weapon(game_state, Supply.SNIPER)
    else:
        message = 'What survivors should do[0/1]?\n' \
                  '[0]: kill big zombie\n' \
                  '[1]: kill lesser zombie\n>>'
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            play_weapon(game_state, Supply.SNIPER, strong=True)
        else:
            play_weapon(game_state, Supply.SNIPER)


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
            shelter.print('New survivor has arrived at your shelter!')
            shelter.survivors.append(card)
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


def play_obstacle(game_state, obstacle):
    shelter = game_state.active_player
    shelter.print(f'One of survivors constructed an {obstacle.value} inside the shelter!')
    shelter.supplies.remove(obstacle)
    shelter.obstacles.append(obstacle)


def play_alarm(game_state):
    play_obstacle(game_state, Supply.ALARM)


def defend_with_alarm(game_state):
    shelter = game_state.active_player
    shelter.print(f'One of survivors used {Supply.ALARM.value}!')
    shelter.print(f'The sounds of the {Supply.ALARM.value} could be heard from miles away!')
    for zombie in shelter.zombies:
        zombie.active = False
    shelter.print(f'Thanks to {Supply.ALARM.value} all survivors has managed to hide and are safe!')
    put_supplies_on_graveyard(game_state, Supply.ALARM, obstacle=True)


def play_barricades(game_state):
    play_obstacle(game_state, Supply.BARRICADES)


def defend_with_barricades(game_state):
    shelter = game_state.active_player
    shelter.print(f'There are {Supply.BARRICADES.value} inside shelter!')
    for zombie in shelter.zombies:
        if zombie.active:
            shelter.print(f'{Supply.BARRICADES.value} has stopped {zombie.top.value}')
            zombie.active = False
            put_supplies_on_graveyard(game_state, Supply.BARRICADES, obstacle=True)
            break


def play_mine_field(game_state):
    play_obstacle(game_state, Supply.MINE_FILED)


def defend_with_mine_field(game_state):
    shelter = game_state.active_player
    for count in range(2):
        big_inside, lesser_counter = count_zombies(game_state)
        if len(shelter.zombies) < (3 - count) or (big_inside and lesser_counter == 0) or not big_inside:
            shelter.print(f'{str(shelter.zombies[0].top.value).capitalize()} was wiped out in a mine explosion!')
            shelter.print(f'The sounds of the {Supply.MINE_FILED.value} could be heard from miles away!')
            put_zombie_on_graveyard(game_state, shelter.zombies[0])
        elif big_inside and lesser_counter > 0:
            message = 'What survivors should do [0/1]?\n' \
                      '[0]: lure big zombie on mine field\n' \
                      '[1]: lure lesser zombie on mine field\n>>'
            action = get_action(game_state, message, ['0', '1'])
            if action == '0':
                zombie_type = [ZombieType.BIG]
            else:
                zombie_type = [ZombieType.FAST, ZombieType.ZOMBIE]
            for zombie in shelter.zombies:
                if zombie.top in zombie_type:
                    shelter.print(f'{str(zombie.top.value).capitalize()} was wiped out in a mine explosion!')
                    shelter.print(f'The sounds of the {Supply.MINE_FILED.value} could be heard from miles away!')
                    put_zombie_on_graveyard(game_state, zombie)
                    break
    put_supplies_on_graveyard(game_state, Supply.MINE_FILED, obstacle=True)


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


def play_sacrifice(game_state):
    shelter = game_state.active_player
    survivor_card = shelter.survivors[0]
    shelter.survivors.remove(survivor_card)
    game_state.city_graveyard.append(survivor_card)
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)

    for _ in range(len(shelter.zombies)):
        zombie_card = shelter.zombies[0]
        message = f'Where {zombie_card.top.value} will be lured?\n' + choice_message
        action = get_action(game_state, message, possible_actions)
        shelter.zombies.remove(zombie_card)
        rivals[int(action)].zombies.append(zombie_card)
    shelter.print('One of survivors in a heroic act led all the zombies out of the shelter!')
    put_supplies_on_graveyard(game_state, Supply.SACRIFICE)


def play_drone(game_state):
    shelter = game_state.active_player
    big_inside, lesser_counter = count_zombies(game_state)
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)
    if len(shelter.zombies) < 2 or (big_inside and lesser_counter == 0) or not big_inside:
        zombie_card = shelter.zombies[0]
        shelter.print(f'One of survivors used {Supply.DRONE} to lure {zombie_card.top.value} out...')
        message = f'Where {zombie_card.top.value} will be lured?\n' + choice_message
        action = get_action(game_state, message, possible_actions)
        shelter.zombies.remove(zombie_card)
        rivals[int(action)].zombies.append(zombie_card)

    elif big_inside and lesser_counter > 0:
        message = 'What survivors should do [0/1]?\n' \
                  '[0]: lure big zombie out of shelter\n' \
                  '[1]: lure lesser zombie out of shelter\n>>'
        action = get_action(game_state, message, ['0', '1'])
        if action == '0':
            zombie_type = [ZombieType.BIG]
        else:
            zombie_type = [ZombieType.FAST, ZombieType.ZOMBIE]
        for zombie in shelter.zombies:
            if zombie.top in zombie_type:
                shelter.print(f'One of survivors used {Supply.DRONE.value} to lure {zombie.top.value} out...')
                message = f'Where {zombie.top.value} will be lured?\n' + choice_message
                action = get_action(game_state, message, possible_actions)
                shelter.zombies.remove(zombie)
                rivals[int(action)].zombies.append(zombie)
                break
    put_supplies_on_graveyard(game_state, Supply.DRONE)


def play_chainsaw(game_state):
    shelter = game_state.active_player
    rivals = []
    choice_message = ''
    possible_actions = []
    for rival in game_state.players:
        if rival != shelter and not rival.defeated and len(rival.obstacles) > 0:
            rivals.append(rival)
    for index, rival in enumerate(rivals):
        choice_message += f'[{index}]: {rival.name} shelter\n'
        possible_actions.append(str(index))
    if len(rivals) > 0:
        message = f'Where survivor should use {Supply.CHAINSAW.value} to destroy fortifications?\n' + choice_message
        action = get_action(game_state, message, possible_actions)
        rival = rivals[int(action)]
        shelter.print(f'Survivor successfully destroyed all defence at {rival.name} shelter!')
        for _ in range(len(rival.obstacles)):
            obstacle = rival.obstacles[0]
            rival.obstacles.remove(obstacle)
            game_state.supply_graveyard.append(obstacle)
    shelter.print(f'The sounds of the {Supply.CHAINSAW.value} could be heard from miles away!')
    put_supplies_on_graveyard(game_state, Supply.CHAINSAW)


def play_takeover(game_state):
    shelter = game_state.active_player
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)
    message = 'From which shelter lure a survivor to join us?\n' + choice_message
    action = get_action(game_state, message, possible_actions)
    rival = rivals[int(action)]
    survivor_card = rival.survivors[0]
    rival.survivors.remove(survivor_card)
    if len(rival.survivors) == 0:
        shelter.print(f'No one was left in {rival.name} shelter...')
        rival.defeated = True
    shelter.survivors.append(survivor_card)
    put_supplies_on_graveyard(game_state, Supply.TAKEOVER)
