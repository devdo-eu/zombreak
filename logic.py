from random import shuffle


class PlayerShelter:
    def __init__(self, name=''):
        self.name = name
        self.survivors = []
        self.supplies = []
        self.obstacles = []
        self.zombies = []
        self.defeated = False


class GameState:
    def __init__(self):
        self.city_deck = []
        self.supply_deck = []
        self.city_graveyard = []
        self.supply_graveyard = []
        self.players = []
        self.active_player = None
        self.finished = False

    @property
    def players_still_in_game(self):
        return [player for player in self.players if not player.defeated]

    def prepare_city_deck(self):
        horde = ['horde'] * 2
        zombie = ['zombie'] * 23
        fast = ['fast zombie'] * 18
        big = ['big zombie'] * 12
        zombies = horde + zombie + fast + big
        deck = []
        for card in zombies:
            deck.append(['survivor', card])
        shuffle(deck)
        self.city_deck = deck

    def shuffle_city_graveyard(self):
        new_city = []
        for card in self.city_graveyard:
            if card[0] == 'survivor':
                new_city.append(card)
            else:
                card[0], card[1] = card[1], card[0]
                new_city.append(card)
        shuffle(new_city)
        self.city_graveyard = []
        self.city_deck = self.city_deck + new_city

    def get_city_card(self):
        if len(self.city_deck) < 1:
            self.shuffle_city_graveyard()
        if len(self.city_deck) < 1:
            return None
        card = self.city_deck.pop(0)
        return card

    def shuffle_supply_graveyard(self):
        new_supplies = self.supply_graveyard
        shuffle(new_supplies)
        self.supply_graveyard = []
        self.supply_deck = self.supply_deck + new_supplies

    def get_supply_card(self):
        if len(self.supply_deck) < 1:
            self.shuffle_supply_graveyard()
        if len(self.supply_deck) < 1:
            return None
        card = self.supply_deck.pop(0)
        return card

    def prepare_supply_deck(self):
        defense = ['alarm'] * 2 + ['mine field'] * 2 + ['barricades'] * 4
        summons = ['radio'] * 4 + ['megaphone'] * 4 + ['flare gun'] * 3
        counters = ['sacrifice'] * 2 + ['drone'] * 6 + ['lure out'] * 7 + ['destroy defence'] * 2 +\
                   ['takeover'] * 2 + ['swap shelter'] * 2
        killers = ['sniper rifle'] * 2 + ['shotgun'] * 6 + ['axe'] * 3 + ['gun'] * 4
        supply_deck = defense + summons + counters + killers
        shuffle(supply_deck)
        self.supply_deck = supply_deck

    def zombie_show_up(self):
        card = self.get_city_card()
        if card is None:
            return

        if card[0] == 'survivor' and card[1] not in ['fast zombie', 'horde']:
            card[0], card[1] = card[1], card[0]
            self.city_deck = [card] + self.city_deck
            return
        elif card[1] == 'fast zombie':
            card[0], card[1] = card[1], card[0]
        elif card[1] == 'horde':
            self.event_horde()
            self.city_graveyard.append(card)
            return

        self.active_player.zombies.append(card)

    def event_horde(self, second=False):
        index = self.players_still_in_game.index(self.active_player)
        helper_table = self.players_still_in_game + self.players_still_in_game
        helper_table = helper_table[index + 1: index + len(self.players_still_in_game) + 1]

        for player in helper_table:
            card = self.get_city_card()
            if card is None or (second and player == self.active_player):
                continue
            card[0], card[1] = card[1], card[0]
            if card[0] == 'horde':
                self.event_horde(True)
                self.city_graveyard.append(card)
                card = self.get_city_card()
                if card is not None:
                    card[0], card[1] = card[1], card[0]
                    player.zombies.append(card)
            else:
                player.zombies.append(card)

    def get_supplies(self):
        how_many = len(self.active_player.supplies)
        for _ in range(how_many, 3):
            card = self.get_supply_card()
            if card is None:
                break
            self.active_player.supplies.append(card)

    def activate_obstacle(self, obstacle):
        pass

    def clean_up_shelter(self, shelter):
        self.supply_graveyard += shelter.supplies + shelter.obstacles
        self.city_graveyard += shelter.zombies + shelter.survivors
        shelter.supplies, shelter.obstacles, shelter.zombies, shelter.survivors = [], [], [], []

    def end_active_player_turn(self):
        index = self.players.index(self.active_player)
        if len(self.active_player.zombies) != 0:
            for obstacle in self.active_player.obstacles:
                self.activate_obstacle(obstacle)
            for _ in self.active_player.zombies:
                if len(self.active_player.survivors) > 0:
                    card = self.active_player.survivors.pop()
                    self.city_graveyard.append(card)

        if len(self.active_player.survivors) == 0:
            self.active_player.defeated = True
            index -= 1
            self.clean_up_shelter(self.active_player)
        else:
            self.get_supplies()
        helper_table = self.players_still_in_game + self.players_still_in_game
        self.active_player = helper_table[index + 1]
