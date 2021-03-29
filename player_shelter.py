from zombie_enums import ZombieType


class PlayerShelter:
    def __init__(self, name='', input_foo=input, print_foo=print):
        self.name = name
        self.survivors = []
        self.supplies = []
        self.obstacles = []
        self.zombies = []
        self.defeated = False
        self.input = input_foo
        self.print = print_foo
        self.gui = self.gui_default

    def gui_default(self, game_state):
        bar_length = 80
        info = '-' * bar_length + '\n'
        info += f'City: {len(game_state.city_deck)}, City Graveyard: {len(game_state.city_graveyard)}\n'
        info += f'Supplies: {len(game_state.supply_deck)}, Used Supplies Pile: {len(game_state.supply_graveyard)}\n'
        info += '-' * bar_length + '\n'
        rivals = self.get_rivals_list(game_state)
        for rival in rivals:
            if not rival.defeated:
                rival_info = self.get_shelter_info(rival)
                info += rival_info + '-' * bar_length + '\n'

        supplies = self.obstacle_or_supplies_info(self, False)
        city = self.news_from_city(game_state)
        my_info = 'Your ' + self.get_shelter_info(self) + f'Supplies: {supplies[:-2]}\n' + city
        self.print(info + my_info)

    def get_shelter_info(self, shelter):
        big_zombies, lesser_zombies = self.zombie_counter(shelter)
        obstacles = self.obstacle_or_supplies_info(shelter)
        info = f'Shelter: {shelter.name}\n' \
               f'Survivors: {len(shelter.survivors)}\n' \
               f'Obstacles: {obstacles[:-2]}\n' \
               f'All Zombies: {len(shelter.zombies)}, Big: {big_zombies}, Lesser: {lesser_zombies}\n'
        return info

    def get_rivals_list(self, game_state):
        rivals = []
        for player in game_state.players:
            if player.name != self.name:
                rivals.append(player)
        return rivals

    @staticmethod
    def news_from_city(game_state):
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
    def obstacle_or_supplies_info(shelter, obstacle=True):
        info = ''
        objects = shelter.obstacles
        if not obstacle:
            objects = shelter.supplies
        for obj in objects:
            info += f'{obj.value}, '
        return info

    @staticmethod
    def zombie_counter(shelter):
        lesser_zombies = 0
        big_zombies = 0
        for zombie in shelter.zombies:
            if zombie.top == ZombieType.BIG:
                big_zombies += 1
            else:
                lesser_zombies += 1
        return big_zombies, lesser_zombies
