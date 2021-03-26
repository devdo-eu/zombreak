from random import shuffle


class PlayerShelter:
    def __init__(self, name=''):
        self.name = name
        self.survivors = []
        self.supplies = []
        self.zombies = []


class GameState:
    def __init__(self):
        self.city_deck = []
        self.supply_deck = []
        self.city_graveyard = []
        self.supply_graveyard = []
        self.players = []
        self.active_player = None

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
        new_city = self.city_graveyard
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

    def prepare_supply_deck(self):
        defense = ['alarm'] * 2 + ['mine field'] * 2 + ['barricades'] * 4
        summons = ['radio'] * 4 + ['megaphone'] * 4 + ['flare gun'] * 3
        counters = ['sacrifice'] * 2 + ['drones'] * 6 + ['lure out'] * 7 + ['destroy defence'] * 2 +\
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

        self.active_player.zombies.append(card[0])

    def event_horde(self, second=False):
        index = self.players.index(self.active_player)
        helper_table = self.players + self.players
        helper_table = helper_table[index + 1: index + len(self.players) + 1]

        for player in helper_table:
            card = self.get_city_card()
            if card is None or (second and player == self.active_player):
                continue
            if card[1] == 'horde':
                self.event_horde(True)
                self.city_graveyard.append(card)
                card = self.get_city_card()
                if card is not None:
                    player.zombies.append(card[1])
            else:
                player.zombies.append(card[1])
