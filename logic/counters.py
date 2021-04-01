from enums.zombie import ZombieType
from enums.supply import Supply
from logic.common import find_rivals_and_build_action_message, put_supplies_on_graveyard, get_action
from logic.common import count_zombies_and_execute_function


async def play_sacrifice(game_state):
    shelter = game_state.active_player
    survivor_card = shelter.survivors[0]
    shelter.survivors.remove(survivor_card)
    game_state.city_graveyard.append(survivor_card)
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)

    for _ in range(len(shelter.zombies)):
        zombie_card = shelter.zombies[0]
        message = f'Where {zombie_card.top.value} will be lured?\n' + choice_message
        action = await get_action(game_state, message, possible_actions)
        shelter.zombies.remove(zombie_card)
        rivals[int(action)].zombies.append(zombie_card)
    shelter.print('One of survivors in a heroic act led all the zombies out of the shelter!')
    put_supplies_on_graveyard(game_state, Supply.SACRIFICE)


async def play_drone(game_state):
    shelter = game_state.active_player
    if len(shelter.zombies) == 0:
        shelter.print(f'You cannot use {Supply.DRONE.value} for nothing...')
    else:
        async def use_drone(zombie):
            choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)
            shelter.print(f'One of survivors used {Supply.DRONE.value} to lure {zombie.top.value} out...')
            message = f'Where {zombie.top.value} will be lured?\n' + choice_message
            action = await get_action(game_state, message, possible_actions)
            shelter.zombies.remove(zombie)
            shelter.print(f'{str(zombie.top.value).capitalize()} was lured to "{rivals[int(action)].name}" shelter!')
            rivals[int(action)].zombies.append(zombie)

        message = 'What survivors should do [0/1]?\n[0]: lure big zombie out of shelter\n' \
                  '[1]: lure lesser zombie out of shelter\n>'
        await count_zombies_and_execute_function(game_state, message, use_drone)
        put_supplies_on_graveyard(game_state, Supply.DRONE)


async def play_chainsaw(game_state):
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
        message = f'Where survivor should use {Supply.CHAINSAW.value} to destroy fortifications?\n>' + choice_message
        action = await get_action(game_state, message, possible_actions)
        rival = rivals[int(action)]
        shelter.print(f'Survivor successfully destroyed all defence at {rival.name} shelter!')
        for _ in range(len(rival.obstacles)):
            obstacle = rival.obstacles[0]
            rival.obstacles.remove(obstacle)
            game_state.supply_graveyard.append(obstacle)
    shelter.print(f'The sounds of the {Supply.CHAINSAW.value} could be heard from miles away!')
    put_supplies_on_graveyard(game_state, Supply.CHAINSAW)


async def play_takeover(game_state):
    shelter = game_state.active_player
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)
    message = 'From which shelter lure a survivor to join us?\n' + choice_message
    action = await get_action(game_state, message, possible_actions)
    rival = rivals[int(action)]
    survivor_card = rival.survivors[0]
    shelter.print(f'Survivor from {rival.name} shelter join to us!')
    rival.survivors.remove(survivor_card)
    if len(rival.survivors) == 0:
        shelter.print(f'No one was left in {rival.name} shelter...')
        rival.defeated = True
    shelter.survivors.append(survivor_card)
    put_supplies_on_graveyard(game_state, Supply.TAKEOVER)


async def play_swap(game_state):
    shelter = game_state.active_player
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)
    message = 'Which player do you want to swap shelters with?\n' + choice_message
    action = await get_action(game_state, message, possible_actions)
    rival = rivals[int(action)]
    shelter.zombies, rival.zombies = rival.zombies, shelter.zombies
    shelter.print(f'Your survivors used {Supply.SWAP.value} to swap shelters with {rival.name}')
    shelter.obstacles, rival.obstacles = rival.obstacles, shelter.obstacles
    shelter.print(f'The sounds of the {Supply.SWAP.value} could be heard from miles away!')
    put_supplies_on_graveyard(game_state, Supply.SWAP)


async def play_lure_out(game_state):
    shelter = game_state.active_player
    choice_message, possible_actions, rivals = find_rivals_and_build_action_message(game_state)
    used = False
    if len(game_state.city_deck) > 0:
        top_card = game_state.city_deck[0]
        if top_card.top != ZombieType.SURVIVOR:
            zombie_cap = str(top_card.top.value).capitalize()
            message = f'{zombie_cap} is in the city. Should the survivors lure it to rival shelter[y/n]?\n>'
            action = await get_action(game_state, message, ['y', 'n'])
            if action == 'y':
                message = 'Which shelter should the survivors lure the zombies into?\n' + choice_message
                action = await get_action(game_state, message, possible_actions)
                rival = rivals[int(action)]
                card = game_state.get_city_card()
                shelter.print(f'One of survivors lure {card.top.value} from city into {rival.name} shelter!')
                rival.zombies.append(card)
                used = True

    if len(shelter.zombies) > 0:
        message = 'What survivors should do [0/1]?\n[0]: lure big zombie out of shelter\n' \
                  '[1]: lure lesser zombie out of shelter\n>'

        async def lure_out(zombie_card):
            shelter.print(f'One of survivors used {Supply.LURE_OUT.value} to lure {zombie_card.top.value} out...')
            message = f'Where {zombie_card.top.value} will be lured?\n' + choice_message
            action = await get_action(game_state, message, possible_actions)
            rival = rivals[int(action)]
            rival.zombies.append(zombie_card)
            shelter.print(f'One of survivors lure {zombie_card.top.value} from our shelter into {rival.name} shelter!')
            shelter.zombies.remove(zombie_card)

        await count_zombies_and_execute_function(game_state, message, lure_out)
        put_supplies_on_graveyard(game_state, Supply.LURE_OUT)
    elif used:
        put_supplies_on_graveyard(game_state, Supply.LURE_OUT)
    else:
        shelter.print(f'You cannot use {Supply.LURE_OUT.value} for nothing...')
