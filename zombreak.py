import game_state


def main(print_foo=print, input_foo=input):
    print_foo('Welcome to Zombreak game!')
    how_many = int(input_foo('How many players will play?: '))
    if how_many < 2:
        raise Exception('Wrong number of players!')
    initial_survivors = int(input_foo('How many survivors on start?: '))
    if initial_survivors < 1 or how_many * initial_survivors > 25:
        raise Exception('Wrong number of initial survivors!')
    names = []
    for index in range(how_many):
        names.append(input_foo(f'Enter name for player #{index}: '))
    game = game_state.GameState()
    game.setup_game(names, initial_survivors)
    winners = game.play_game()
    if len(winners) > 0:
        print_foo(f'Game won by: {winners}')
    else:
        print_foo('All shelters destroyed. Zombies won!')


if __name__ == '__main__':
    main()