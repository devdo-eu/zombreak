from logic import game_state
import asyncio
from collections.abc import Callable


async def main(print_foo: Callable[[str], None] = print, input_foo: Callable[[str], str] = input) -> None:
    """
    Function used to setup and enter the zombreak game from terminal.
    :param print_foo: functor with function used to show output to user
    :param input_foo: functor with function used to get input from user
    """
    print_foo('Welcome to Zombreak game!')
    how_many = int(input_foo('How many players will play? (2-6): '))
    if how_many < 2 or how_many > 6:
        raise Exception('Wrong number of players!')
    initial_survivors = int(input_foo('How many survivors on start? (1-3): '))
    if initial_survivors < 1 or initial_survivors > 3:
        raise Exception('Wrong number of initial survivors!')
    names = []
    for index in range(how_many):
        names.append(input_foo(f'Enter name for player #{index}: '))
    game = game_state.GameState()
    game.setup_game(names, initial_survivors)
    winners = await game.play_game()
    if len(winners) > 0:
        print_foo(f'Game won by: {winners}')
    else:
        print_foo('All shelters destroyed. Zombies won!')


if __name__ == '__main__':
    asyncio.run(main())
