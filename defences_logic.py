from zombie_enums import ZombieType
from supply_enums import Supply
from common_logic import put_zombie_on_graveyard, put_supplies_on_graveyard, count_zombies, get_action


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
