from enums.zombie import ZombieType
from enums.supply import Supply, SupplyType
from collections.abc import Callable, Awaitable
from typing import Any


def is_loud(supply: Supply) -> bool:
    """
    Helper function used to return information if given supply is a loud one.
    :param supply: Supply enum with supply card chose to check
    :return: True if supply is loud, False otherwise
    """
    loud_supplies = [Supply.MEGAPHONE, Supply.FLARE_GUN, Supply.CHAINSAW, Supply.SWAP, Supply.SHOTGUN, Supply.GUN]
    return supply in loud_supplies


def loud_obstacle(supply: Supply) -> bool:
    """
    Helper function used to return information if given obstacle is a loud one.
    :param supply: Supply enum with obstacle card chose to check
    :return:
    """
    return supply in [Supply.ALARM, Supply.MINE_FILED]


def check_type(supply: Supply) -> SupplyType:
    """
    Helper function used to translate Supply enum to SupplyType enum.
    :param supply: Supply enum with card chose to check
    :return: SupplyType of given Supply
    """
    if supply in [Supply.ALARM, Supply.MINE_FILED, Supply.BARRICADES]:
        return SupplyType.DEFENCE
    elif supply in [Supply.RADIO, Supply.MEGAPHONE, Supply.FLARE_GUN]:
        return SupplyType.SUMMON
    elif supply in [Supply.SNIPER, Supply.SHOTGUN, Supply.GUN, Supply.AXE]:
        return SupplyType.WEAPON
    else:
        return SupplyType.COUNTER


def put_supplies_on_graveyard(game_state, supply: Supply, obstacle: bool = False) -> None:
    """
    Helper function used to put given supply card on supply_graveyard list
    :param game_state: GameState object with all game data inside
    :param supply: Supply enum with card which should be put on graveyard
    :param obstacle: flag indicator if given supply was obstacle inside shelter
    """
    shelter = game_state.active_player
    shelter.print(f'{str(supply.value).capitalize()} has been destroyed!')
    if not obstacle:
        shelter.supplies.remove(supply)
    else:
        shelter.obstacles.remove(supply)
    game_state.supply_graveyard.append(supply)


def put_zombie_on_graveyard(game_state, zombie_card) -> None:
    """
    Helper function used to put given city card on city_graveyard list.
    :param game_state: GameState object with all game data inside
    :param zombie_card: CityCard object with data about survivor or zombie
    """
    shelter = game_state.active_player
    shelter.zombies.remove(zombie_card)
    game_state.city_graveyard.append(zombie_card)


async def get_action(game_state, message: str, possible_actions: list) -> int:
    """
    Helper function used to get action from player for current state of game.
    :param game_state: GameState object with all game data inside
    :param message: string with message for player
    :param possible_actions: list with all possible action for given GameState
    :return: int value of chosen action
    """
    shelter = game_state.active_player
    if len(possible_actions) == 1:
        return possible_actions[0]
    while True:
        action = await shelter.input_async(message)
        if action in possible_actions:
            break
        else:
            shelter.print(f'No such action as {action}!')
    return action


def find_rivals_and_build_action_message(game_state) -> tuple[str, list[str], list]:
    """
    Helper function used to build message for current player when there is a need to choose target for played card.
    :param game_state: GameState object with all game data inside
    :return: tuple with string message to be shown to player, list of possible actions and list of rivals
    """
    shelter = game_state.active_player
    rivals, possible_actions = [], []
    choice_message = ''
    for rival in game_state.players_still_in_game:
        if rival != shelter and not rival.defeated:
            rivals.append(rival)
    for index, rival in enumerate(rivals):
        choice_message += f'[{index}]: "{rival.name}" shelter\n'
        possible_actions.append(str(index))
    choice_message += '>'
    return choice_message, possible_actions, rivals


def count_zombies(game_state) -> tuple[bool, int]:
    """
    Helper function used to check if inside shelter is one or more big zombies and count of all lesser zombies.
    :param game_state: GameState object with all game data inside
    :return: tuple with bool flag if inside is big zombie and int value with sum of all lesser zombies inside shelter
    """
    shelter = game_state.active_player
    big_inside = False
    lesser_counter = 0
    for zombie_card in shelter.zombies:
        if zombie_card.top == ZombieType.BIG:
            big_inside = True
        else:
            lesser_counter += 1
    return big_inside, lesser_counter


async def count_zombies_and_execute_function(game_state, message: str, execute: Callable[[Any], Awaitable[None]],
                                             count: int = 2) -> None:
    """
    Helper function used to depending on the circumstances execute param function
    or ask player on which zombie execute param function.
    :param game_state: GameState object with all game data inside
    :param message: string with message for player
    :param execute: callable function with CityCard param
    :param count: how many times function should be called
    """
    shelter = game_state.active_player
    big_inside, lesser_counter = count_zombies(game_state)
    if len(shelter.zombies) == 0:
        return
    elif len(shelter.zombies) < count or (big_inside and lesser_counter == 0) or not big_inside:
        zombie_card = shelter.zombies[0]
        await execute(zombie_card)
    else:
        action = await get_action(game_state, message, ['0', '1'])
        if action == '0':
            zombie_type = [ZombieType.BIG]
        else:
            zombie_type = [ZombieType.FAST, ZombieType.ZOMBIE]
        for zombie in shelter.zombies:
            if zombie.top in zombie_type:
                zombie_card = zombie
                await execute(zombie_card)
                break
