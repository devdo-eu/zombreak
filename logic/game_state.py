from random import shuffle
from enums.zombie import ZombieType
from enums.supply import Supply
from logic.city_card import CityCard
from player.player_shelter import PlayerShelter
from player.cpu_player_shelter import CPUPlayerShelter
from copy import copy
from logic import common, counters, defences, summons, weapons

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
        self.last_supplies_taken = False
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
            return None
        card = self.city_deck.pop(0)
        if len(self.city_deck) == 0:
            self.final_attack = True
        return card

    def shuffle_supply_graveyard(self):
        new_supplies = self.supply_graveyard
        shuffle(new_supplies)
        self.supply_graveyard = []
        self.supply_deck = self.supply_deck + new_supplies

    def get_supply_card(self):
        if len(self.supply_deck) < 1:
            self.shuffle_supply_graveyard()
        if len(self.supply_deck) < 1 or (self.final_attack and self.last_supplies_taken):
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
            self.active_player.print(f'{str(card.top.value).capitalize()} has appeared in city!')
            return
        elif card.bottom == ZombieType.FAST:
            card.flip()
        elif card.bottom == ZombieType.HORDE:
            self.active_player.print('A terrifying zombie horde has engulfed the city!')
            self.event_horde()
            self.city_graveyard.append(card)
            return

        self.active_player.print(f'{str(card.top.value).capitalize()} has entered "{self.active_player.name}" shelter!')
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
                    player.print(f'{str(card.top.value).capitalize()} has entered {player.name} shelter!')
                    player.zombies.append(card)
            else:
                player.print(f'{str(card.top.value).capitalize()} has entered {player.name} shelter!')
                player.zombies.append(card)

    def get_supplies(self):
        how_many = len(self.active_player.supplies)
        for _ in range(how_many, 3):
            card = self.get_supply_card()
            if card is None:
                break
            self.active_player.supplies.append(card)
        if self.final_attack:
            self.last_supplies_taken = True

    async def activate_obstacle(self, obstacle):
        await activate_obstacle[obstacle](self)

    def clean_up_shelter(self, shelter):
        self.supply_graveyard += shelter.supplies + shelter.obstacles
        self.city_graveyard += shelter.zombies + shelter.survivors
        shelter.supplies, shelter.obstacles, shelter.zombies, shelter.survivors = [], [], [], []

    async def end_active_player_turn(self):
        index = self.players_still_in_game.index(self.active_player)
        loud_defence = await self.defend_with_obstacles()
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
            self.active_player.print(f'No more living survivors inside "{self.active_player.name}" shelter...')
            self.active_player.defeated = True
            index -= 1
        else:
            self.get_supplies()
            if loud_defence:
                self.active_player.print('Loud noises in your shelter could be heard from miles away...')
                self.zombie_show_up()
            self.active_player.print(f'{self.active_player.name} turn has ended.')
        self.clean_up_table()
        return index

    def zombies_eats_survivors(self):
        shelter = self.active_player
        for zombie in shelter.zombies:
            if len(shelter.survivors) > 0 and zombie.active:
                zombie_cap = str(zombie.top.value).capitalize()
                shelter.print(f'{zombie_cap} killed survivor! '
                              f'{len(shelter.survivors)} left inside "{shelter.name}" shelter')
                card = shelter.survivors.pop()
                self.city_graveyard.append(card)

    async def defend_with_obstacles(self):
        loud_defence = False
        obstacles = copy(self.active_player.obstacles)
        for obstacle in obstacles:
            if len(self.active_player.zombies) != 0 and self.active_player_active_zombies:
                action = await common.get_action(self, f'Do you want to use {obstacle.value}[y/n]?\n>', ['y', 'n'])
                if action == 'y':
                    await self.activate_obstacle(obstacle)
                    if common.loud_obstacle(obstacle):
                        loud_defence = True
        return loud_defence

    async def play_round(self):
        shelter = self.active_player
        shelter.card_used_or_discarded = False
        opening_supplies = len(shelter.supplies)
        shelter.print(f'{shelter.name} will play round now...')
        for zombie in shelter.zombies:
            zombie.active = True

        turn_end = False
        discarded = False
        while len(shelter.supplies) > 0 and not turn_end:
            shelter.gui(self)
            self.clean_up_table()
            if discarded:
                turn_end = await self.discard_supplies_move(turn_end)
                continue

            action, possible_actions = await self.ask_player_what_move()
            if action in possible_actions[:-1]:
                loud = common.is_loud(shelter.supplies[int(action)])
                await play_supplies[shelter.supplies[int(action)]](self)
                if loud:
                    self.zombie_show_up()
            elif action == possible_actions[-1] and not shelter.card_used_or_discarded:
                discarded = True
                turn_end = await self.discard_supplies_move(turn_end)
            else:
                turn_end = True

            if opening_supplies > len(shelter.supplies):
                shelter.card_used_or_discarded = True

            if len(shelter.survivors) == 0 or len(self.players_still_in_game) < 2:
                turn_end = True
        await self.end_active_player_turn()

    def clean_up_table(self):
        for player in self.players:
            if len(player.survivors) == 0:
                player.defeated = True
            not_clean = len(player.supplies) > 0 or len(player.zombies) > 0 or len(player.obstacles) > 0
            if player.defeated and not_clean:
                self.clean_up_shelter(player)

    async def ask_player_what_move(self):
        shelter = self.active_player
        possible_actions = [str(number) for number in range(len(shelter.supplies) + 1)]
        question = 'What do you want to do?\n'
        for index, supply in enumerate(shelter.supplies):
            loud = ''
            if common.is_loud(supply):
                loud = '(loud instantly)'
            elif common.loud_obstacle(supply):
                loud = '(loud after use in defence phase)'
            question += f'[{index}] Use {supply.value} {loud}\n'
        if not shelter.card_used_or_discarded:
            question += f'[{len(shelter.supplies)}] Discard some supplies\n'
        else:
            question += f'[{len(shelter.supplies)}] End my turn\n'
        action = await common.get_action(self, question + '> ', possible_actions)
        return action, possible_actions

    async def discard_supplies_move(self, turn_end):
        shelter = self.active_player
        possible_actions = [str(number) for number in range(len(shelter.supplies) + 1)]
        question = 'Which supply you want to discard?\n'
        for index, supply in enumerate(shelter.supplies):
            question += f'[{index}] Discard {supply.value}\n'
        if not shelter.card_used_or_discarded:
            question += f'[{len(shelter.supplies)}] Discard all supplies\n'
        else:
            question += f'[{len(shelter.supplies)}] End my turn\n'
        action = await common.get_action(self, question + '> ', possible_actions)
        if action in possible_actions[:-1]:
            self.supply_graveyard.append(shelter.supplies.pop(int(action)))
        elif action == possible_actions[-1] and len(shelter.supplies) == 3:
            for _ in range(len(shelter.supplies)):
                self.supply_graveyard.append(shelter.supplies.pop())
            shelter.print(f'{shelter.name} discards all supplies.')
            turn_end = True
        else:
            turn_end = True
        return turn_end

    def setup_game(self, players_names, initial_survivors=2):
        self.prepare_city_deck()
        self.prepare_supply_deck()
        self.players = []
        for name in players_names:
            if 'CPU' in name:
                shelter = CPUPlayerShelter(name)
            else:
                shelter = PlayerShelter(name)
            for _ in range(initial_survivors):
                shelter.survivors.append(self.get_city_card())
            for _ in range(3):
                shelter.supplies.append(self.get_supply_card())
            self.players.append(shelter)
        self.active_player = self.players[0]

    async def play_game(self):
        while not self.finished:
            await self.play_round()
        winners = self.get_winners()
        return winners

    def get_winners(self):
        winners = []
        survivors_amount = []
        for shelter in self.players:
            if len(shelter.survivors) > 0:
                survivors_amount.append(len(shelter.survivors))
        if len(survivors_amount) > 0:
            max_survivors = max(survivors_amount)
            for shelter in self.players:
                if len(shelter.survivors) == max_survivors:
                    winners.append(shelter.name)
        return winners
