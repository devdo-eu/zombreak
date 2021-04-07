from enums.supply import Supply
from logic.common import put_zombie_on_graveyard, put_supplies_on_graveyard, count_zombies_and_execute_function


async def play_obstacle(game_state, obstacle: Supply) -> None:
    """
    Function used to control of play on table of any obstacle card.
    :param game_state: GameState object with all game data inside
    :param obstacle: Supply enum with played card
    """
    shelter = game_state.active_player
    shelter.print(f'One of survivors constructed an {obstacle.value} inside the shelter!')
    shelter.supplies.remove(obstacle)
    shelter.obstacles.append(obstacle)


async def play_alarm(game_state) -> None:
    """
    Function used to control of play of ALARM card.
    :param game_state: GameState object with all game data inside
    """
    await play_obstacle(game_state, Supply.ALARM)


async def defend_with_alarm(game_state) -> None:
    """
    Function used to control of defend phase with ALARM card.
    :param game_state: GameState object with all game data inside
    """
    shelter = game_state.active_player
    shelter.print(f'One of survivors used {Supply.ALARM.value}!')
    shelter.print(f'The sounds of the {Supply.ALARM.value} could be heard from miles away!')
    for zombie in shelter.zombies:
        zombie.active = False
    shelter.print(f'Thanks to {Supply.ALARM.value} all survivors has managed to hide and are safe!')
    put_supplies_on_graveyard(game_state, Supply.ALARM, obstacle=True)


async def play_barricades(game_state) -> None:
    """
    Function used to control of play of BARRICADES card.
    :param game_state: GameState object with all game data inside
    """
    await play_obstacle(game_state, Supply.BARRICADES)


async def defend_with_barricades(game_state) -> None:
    """
    Function used to control of defend phase with BARRICADES card.
    :param game_state: GameState object with all game data inside
    """
    shelter = game_state.active_player
    shelter.print(f'There are {Supply.BARRICADES.value} inside shelter!')
    for zombie in shelter.zombies:
        if zombie.active:
            shelter.print(f'{Supply.BARRICADES.value} has stopped {zombie.top.value}')
            zombie.active = False
            put_supplies_on_graveyard(game_state, Supply.BARRICADES, obstacle=True)
            break


async def play_mine_field(game_state) -> None:
    """
    Function used to control of play of MINE FIELD card.
    :param game_state: GameState object with all game data inside
    """
    await play_obstacle(game_state, Supply.MINE_FILED)


async def defend_with_mine_field(game_state) -> None:
    """
    Function used to control of defend phase with MINE FIELD card.
    :param game_state: GameState object with all game data inside
    """
    shelter = game_state.active_player

    async def use_mine_field(zombie) -> None:
        """
        Helper function used to play MINE FIELD card at defend phase and get chosen action from player.
        :param zombie: CityCard object with zombie on top.
        """
        shelter.print(f'{str(zombie.top.value).capitalize()} was wiped out in a mine explosion!')
        shelter.print(f'The sounds of the {Supply.MINE_FILED.value} could be heard from miles away!')
        put_zombie_on_graveyard(game_state, zombie)

    message = 'What survivors should do [0/1]?\n[0]: lure big zombie on mine field\n' \
              '[1]: lure lesser zombie on mine field\n>'
    for count in range(2):
        await count_zombies_and_execute_function(game_state, message, use_mine_field, (3 - count))
    put_supplies_on_graveyard(game_state, Supply.MINE_FILED, obstacle=True)
