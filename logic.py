from random import shuffle
from zombie_enums import ZombieType
from supply_enums import Supply
from copy import copy
import weapons_logic
import defences_logic
import counters_logic
import summons_logic
import common_logic


play_supplies = {
    Supply.ALARM: defences_logic.play_alarm,
    Supply.MINE_FILED: defences_logic.play_mine_field,
    Supply.BARRICADES: defences_logic.play_barricades,
    Supply.RADIO: summons_logic.play_radio,
    Supply.MEGAPHONE: summons_logic.play_megaphone,
    Supply.FLARE_GUN: summons_logic.play_flare_gun,
    Supply.SACRIFICE: counters_logic.play_sacrifice,
    Supply.DRONE: counters_logic.play_drone,
    Supply.LURE_OUT: counters_logic.play_lure_out,
    Supply.CHAINSAW: counters_logic.play_chainsaw,
    Supply.TAKEOVER: counters_logic.play_takeover,
    Supply.SWAP: counters_logic.play_swap,
    Supply.SNIPER: weapons_logic.play_sniper_rifle,
    Supply.SHOTGUN: weapons_logic.play_shotgun,
    Supply.GUN: weapons_logic.play_gun,
    Supply.AXE: weapons_logic.play_axe
}

activate_obstacle = {
    Supply.ALARM: defences_logic.defend_with_alarm,
    Supply.BARRICADES: defences_logic.defend_with_barricades,
    Supply.MINE_FILED: defences_logic.defend_with_mine_field
}


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


class CityCard:
    def __init__(self, zombie=ZombieType.ZOMBIE):
        if zombie == ZombieType.SURVIVOR:
            raise Exception('Card cannot be init with survivor on top!')
        self.active = True
        self.top = ZombieType.SURVIVOR
        self.bottom = zombie

    def flip(self):
        self.top, self.bottom = self.bottom, self.top


class GameState:
    def __init__(self):
        self.city_deck = []
        self.supply_deck = []
        self.city_graveyard = []
        self.supply_graveyard = []
        self.players = []
        self.active_player = None
        self.final_attack = False
        self.finished = False

    @property
    def players_still_in_game(self):
        return [player for player in self.players if not player.defeated]

    @property
    def active_player_active_zombies(self):
        for zombie in self.active_player.zombies:
            if zombie.active:
                return True
        return False

    def prepare_city_deck(self):
        horde = [CityCard(ZombieType.HORDE) for _ in range(2)]
        zombie = [CityCard(ZombieType.ZOMBIE) for _ in range(23)]
        fast = [CityCard(ZombieType.FAST) for _ in range(18)]
        big = [CityCard(ZombieType.BIG) for _ in range(12)]
        deck = horde + zombie + fast + big
        shuffle(deck)
        self.city_deck = deck

    def get_city_card(self):
        if len(self.city_deck) < 1:
            self.final_attack = True
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
        if len(self.supply_deck) < 1 or self.final_attack:
            return None
        card = self.supply_deck.pop(0)
        return card

    def prepare_supply_deck(self):
        quantity = [2, 2, 4, 4, 4, 3, 2, 6, 7, 2, 2, 2, 2, 6, 4, 3]
        supply_deck = []
        for index, supply in enumerate(Supply):
            supply_deck += [supply] * quantity[index]
        shuffle(supply_deck)
        self.supply_deck = supply_deck

    def zombie_show_up(self):
        card = self.get_city_card()
        if card is None:
            return

        if card.top == ZombieType.SURVIVOR and card.bottom not in [ZombieType.FAST, ZombieType.HORDE]:
            card.flip()
            self.city_deck = [card] + self.city_deck
            return
        elif card.bottom == ZombieType.FAST:
            card.flip()
        elif card.bottom == ZombieType.HORDE:
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
            card.flip()
            if card.top == ZombieType.HORDE:
                self.event_horde(True)
                self.city_graveyard.append(card)
                card = self.get_city_card()
                if card is not None:
                    card.flip()
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
        activate_obstacle[obstacle](self)

    def clean_up_shelter(self, shelter):
        self.supply_graveyard += shelter.supplies + shelter.obstacles
        self.city_graveyard += shelter.zombies + shelter.survivors
        shelter.supplies, shelter.obstacles, shelter.zombies, shelter.survivors = [], [], [], []

    def end_active_player_turn(self):
        index = self.players.index(self.active_player)
        loud_defence = False
        obstacles = copy(self.active_player.obstacles)
        for obstacle in obstacles:
            if len(self.active_player.zombies) != 0 and self.active_player_active_zombies:
                action = common_logic.get_action(self, f'Do you want to use {obstacle.value}[y/n]?', ['y', 'n'])
                if action == 'y':
                    self.activate_obstacle(obstacle)
                    if common_logic.is_loud(obstacle):
                        loud_defence = True

        for zombie in self.active_player.zombies:
            if len(self.active_player.survivors) > 0 and zombie.active:
                self.active_player.print(f'{str(zombie.top.value).capitalize()} killed survivor!')
                card = self.active_player.survivors.pop()
                self.city_graveyard.append(card)

        if len(self.active_player.survivors) == 0:
            self.active_player.print('No more living survivors inside shelter...')
            self.active_player.defeated = True
            index -= 1
            self.clean_up_shelter(self.active_player)
        else:
            self.get_supplies()
            if loud_defence:
                self.active_player.print('Loud noises in your shelter could be heard from miles away...')
                self.zombie_show_up()
            self.active_player.print('Your turn has ended.')
        helper_table = self.players_still_in_game + self.players_still_in_game
        self.active_player = helper_table[index + 1]
