from random import shuffle
from zombie_enums import ZombieType
from supply_enums import Supply
from city_card import CityCard
from player_shelter import PlayerShelter
from copy import copy
import common_logic
import defences
import summons
import counters
import weapons


play_supplies = {
    Supply.ALARM: defences.play_alarm,
    Supply.MINE_FILED: defences.play_mine_field,
    Supply.BARRICADES: defences.play_barricades,
    Supply.RADIO: summons.play_radio,
    Supply.MEGAPHONE: summons.play_megaphone,
    Supply.FLARE_GUN: summons.play_flare_gun,
    Supply.SACRIFICE: counters.play_sacrifice,
    Supply.DRONE: counters.play_drone,
    Supply.LURE_OUT: counters.play_lure_out,
    Supply.CHAINSAW: counters.play_chainsaw,
    Supply.TAKEOVER: counters.play_takeover,
    Supply.SWAP: counters.play_swap,
    Supply.SNIPER: weapons.play_sniper_rifle,
    Supply.SHOTGUN: weapons.play_shotgun,
    Supply.GUN: weapons.play_gun,
    Supply.AXE: weapons.play_axe
}

activate_obstacle = {
    Supply.ALARM: defences.defend_with_alarm,
    Supply.BARRICADES: defences.defend_with_barricades,
    Supply.MINE_FILED: defences.defend_with_mine_field
}


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
        loud_defence = self.defend_with_obstacles()
        self.zombies_eats_survivors()
        index = self.move_aftermath(index, loud_defence)
        self.check_if_game_continues()

        if not self.finished:
            helper_table = self.players_still_in_game + self.players_still_in_game
            self.active_player = helper_table[index + 1]

    def check_if_game_continues(self):
        zombies_in_game = 0
        still_in_game = 0
        for player in self.players:
            zombies_in_game += len(player.zombies)
            if not player.defeated:
                still_in_game += 1
        if (zombies_in_game == 0 and self.final_attack) or still_in_game < 2:
            self.finished = True

    def move_aftermath(self, index, loud_defence):
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
        return index

    def zombies_eats_survivors(self):
        for zombie in self.active_player.zombies:
            if len(self.active_player.survivors) > 0 and zombie.active:
                self.active_player.print(f'{str(zombie.top.value).capitalize()} killed survivor!')
                card = self.active_player.survivors.pop()
                self.city_graveyard.append(card)

    def defend_with_obstacles(self):
        loud_defence = False
        obstacles = copy(self.active_player.obstacles)
        for obstacle in obstacles:
            if len(self.active_player.zombies) != 0 and self.active_player_active_zombies:
                action = common_logic.get_action(self, f'Do you want to use {obstacle.value}[y/n]?', ['y', 'n'])
                if action == 'y':
                    self.activate_obstacle(obstacle)
                    if common_logic.loud_obstacle(obstacle):
                        loud_defence = True
        return loud_defence

    def play_round(self):
        shelter = self.active_player
        for zombie in shelter.zombies:
            zombie.active = True

        turn_end = False
        discarded = False
        while len(shelter.supplies) > 0 and not turn_end:
            if discarded:
                turn_end = self.discard_supplies_move(turn_end)
                continue

            action, possible_actions = self.ask_player_what_move()
            if action in possible_actions[:-1]:
                loud = common_logic.is_loud(shelter.supplies[int(action)])
                play_supplies[shelter.supplies[int(action)]](self)
                if loud:
                    self.zombie_show_up()
            elif action == possible_actions[-1] and len(shelter.supplies) == 3:
                discarded = True
                turn_end = self.discard_supplies_move(turn_end)
            else:
                turn_end = True
        self.end_active_player_turn()

    def ask_player_what_move(self):
        shelter = self.active_player
        shelter.gui(self)
        possible_actions = [str(number) for number in range(len(shelter.supplies) + 1)]
        question = 'What do you want to do?\n'
        for index, supply in enumerate(shelter.supplies):
            loud = ''
            if common_logic.is_loud(supply):
                loud = '(loud instantly)'
            elif common_logic.loud_obstacle(supply):
                loud = '(loud after use in defence phase)'
            question += f'[{index}] Use {supply.value} {loud}\n'
        if len(shelter.supplies) > 2:
            question += f'[{len(shelter.supplies)}] Discard some supplies\n'
        else:
            question += f'[{len(shelter.supplies)}] End my turn\n'
        action = common_logic.get_action(self, question + '> ', possible_actions)
        return action, possible_actions

    def discard_supplies_move(self, turn_end):
        shelter = self.active_player
        possible_actions = [str(number) for number in range(len(shelter.supplies) + 1)]
        question = 'Which supply you want to discard?\n'
        for index, supply in enumerate(shelter.supplies):
            question += f'[{index}] Discard {supply.value}\n'
        if len(shelter.supplies) > 2:
            question += f'[{len(shelter.supplies)}] Discard all supplies\n'
        else:
            question += f'[{len(shelter.supplies)}] End my turn\n'
        action = common_logic.get_action(self, question + '> ', possible_actions)
        if action in possible_actions[:-1]:
            self.supply_graveyard.append(shelter.supplies.pop(int(action)))
        elif action == possible_actions[-1] and len(shelter.supplies) == 3:
            for _ in range(len(shelter.supplies)):
                self.supply_graveyard.append(shelter.supplies.pop())
            turn_end = True
        else:
            turn_end = True
        return turn_end

    def setup_game(self, players_names, initial_survivors=2):
        self.prepare_city_deck()
        self.prepare_supply_deck()
        self.players = []
        for name in players_names:
            shelter = PlayerShelter(name)
            for _ in range(initial_survivors):
                shelter.survivors.append(self.get_city_card())
            for _ in range(3):
                shelter.supplies.append(self.get_supply_card())
            self.players.append(shelter)
        self.active_player = self.players[0]

    def play_game(self):
        while not self.finished:
            self.play_round()
        winners = []
        for shelter in self.players:
            if len(shelter.survivors) > 0:
                winners.append(shelter.name)
        return winners
