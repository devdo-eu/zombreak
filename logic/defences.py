from enums.supply import Supply
from logic.common import put_zombie_on_graveyard, put_supplies_on_graveyard, count_zombies_and_execute_function


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

    def use_mine_field(zombie):
        shelter.print(f'{str(zombie.top.value).capitalize()} was wiped out in a mine explosion!')
        shelter.print(f'The sounds of the {Supply.MINE_FILED.value} could be heard from miles away!')
        put_zombie_on_graveyard(game_state, zombie)

    message = 'What survivors should do [0/1]?\n[0]: lure big zombie on mine field\n' \
              '[1]: lure lesser zombie on mine field\n>'
    for count in range(2):
        count_zombies_and_execute_function(game_state, message, use_mine_field, (3 - count))
    put_supplies_on_graveyard(game_state, Supply.MINE_FILED, obstacle=True)
