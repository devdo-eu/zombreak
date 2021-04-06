from enums.zombie import ZombieType
from collections.abc import Callable


class PlayerShelter:
    def __init__(self, name: str = '', input_foo: Callable[[str], str] = input,
                 print_foo: Callable[[str], None] = print) -> None:
        self.name = name
        self.survivors = []
        self.supplies = []
        self.obstacles = []
        self.zombies = []
        self.defeated = False
        self.card_used_or_discarded = False
        self.input = input_foo
        self.print = print_foo
        self.gui = self.gui_default

    async def input_async(self, message: str) -> str:
        """
        Helper method used in async parts of code.
        :param message: string with message to user
        :return: string with input from user
        """
        ret = self.input(message)
        return ret

    def gui_default(self, game_state) -> None:
        """
        Method used to create ui from current game state.
        :param game_state: current state of game with all data
        """
        bar_length = 80
        info = '-' * bar_length + '\n'
        info += f'City: {len(game_state.city_deck)}({len(game_state.city_graveyard)}), ' \
                f'Supplies: {len(game_state.supply_deck)}({len(game_state.supply_graveyard)})\n'
        info += '-' * bar_length + '\n'
        rivals = self.get_rivals_list(game_state)
        for rival in rivals:
            if not rival.defeated:
                rival_info = self.get_shelter_info(rival)
                info += rival_info + '-' * bar_length + '\n'

        city = self.news_from_city(game_state)
        my_info = f'Your {self.get_shelter_info(self)}\n{city}'
        self.print(info + my_info)

    def get_shelter_info(self, shelter) -> str:
        """
        Helper method used to create part of ui where data about players are visible.
        :param shelter: PlayerShelter object with all data about player
        :return: string with created ui information about particular player
        """
        big_zombies, lesser_zombies = self.zombie_counter(shelter)
        obstacles = self.obstacle_info(shelter)
        info = f'Shelter: "{shelter.name}", Obstacles: {obstacles[:-2]}\n' \
               f'Survivors: {len(shelter.survivors)}, All Zombies: {len(shelter.zombies)}, ' \
               f'Big: {big_zombies}, Lesser: {lesser_zombies}\n'
        return info

    def get_rivals_list(self, game_state) -> list:
        """
        Helper method used to build list with all players except this player.
        :param game_state: current state of game with all data
        :return: list with all rivals of this player
        """
        rivals = []
        for player in game_state.players:
            if player.name != self.name:
                rivals.append(player)
        return rivals

    @staticmethod
    def news_from_city(game_state) -> str:
        """
        Helper method used to create ui part with all information about city state.
        :param game_state: current state of game with all data
        :return: string with created part of ui
        """
        city = ''
        deck = game_state.city_deck
        if len(deck) == 0:
            city += 'No one with beating heart left in the city...\n'
        elif deck[0].top == ZombieType.SURVIVOR:
            city += 'City is quiet. Let survivors in the city know about us!\n'
        else:
            zombie_name = str(deck[0].top.value).capitalize()
            city += f'{zombie_name} roam the city. Any noise will cause him to find our shelter!\n'
        return city

    @staticmethod
    def obstacle_info(shelter) -> str:
        """
        Helper method used to create information about obstacles available inside player's shelter.
        :param shelter: PlayerShelter object with all data about player
        :return: string with information about obstacles inside shelter
        """
        info = ''
        for obj in shelter.obstacles:
            info += f'{obj.value}, '
        return info

    @staticmethod
    def zombie_counter(shelter) -> tuple[int, int]:
        """
        Helper method used to calculate how many big and how many lesser zombies are inside players shelter
        :param shelter: PlayerShelter object with all data about player
        :return: tuple with int value of big zombies and int value of lesser zombies
        """
        lesser_zombies = 0
        big_zombies = 0
        for zombie in shelter.zombies:
            if zombie.top == ZombieType.BIG:
                big_zombies += 1
            else:
                lesser_zombies += 1
        return big_zombies, lesser_zombies
