from enums.zombie import ZombieType
from enums.supply import Supply, SupplyType
from player.player_shelter import PlayerShelter
from logic import common
from copy import copy
from secrets import choice


class CPUPlayerShelter(PlayerShelter):
    def __init__(self, name='', print_foo=print):
        PlayerShelter.__init__(self, name, self.cpu_input, print_foo)
        self.gui = self.cpu_ui
        self.move_counter = -1
        self.planned_moves = []
        self.game_state = None

    @property
    def zombie_amount(self):
        return len(self.zombies)

    @property
    def obstacle_amount(self):
        return len(self.obstacles)

    @property
    def supply_amount(self):
        return len(self.supplies)

    @property
    def city_amount(self):
        return len(self.game_state.city_deck)

    @property
    def zombie_in_city(self):
        if self.city_amount > 0:
            return self.game_state.city_deck[0].top is not ZombieType.SURVIVOR
        else:
            return True

    @property
    def supplies_types(self):
        return [common.check_type(supply) for supply in self.supplies]

    @property
    def weapons_amount(self):
        types = self.supplies_types
        return types.count(SupplyType.WEAPON)

    @property
    def summons_amount(self):
        types = self.supplies_types
        return types.count(SupplyType.SUMMON)

    @property
    def counters_amount(self):
        types = self.supplies_types
        return types.count(SupplyType.COUNTER)

    @property
    def defences_amount(self):
        types = self.supplies_types
        return types.count(SupplyType.DEFENCE)

    @property
    def supplies_loud(self):
        return [common.is_loud(supply) for supply in self.supplies]

    def cpu_input(self, message):
        if '[y/n]?' in message and 'Do you want to use' in message:
            if Supply.BARRICADES.value in message:
                self.defend_with_barricades()
            elif Supply.MINE_FILED.value in message:
                self.defend_with_mine_field()
            else:
                self.defend_with_alarm()
            return self.planned_moves[0]
        else:
            self.move_counter += 1
            if self.move_counter < len(self.planned_moves):
                move = self.planned_moves[self.move_counter]
            else:
                move = str(self.supply_amount)
            return move

    def cpu_ui(self, game_state):
        self.game_state = game_state
        self.move_counter = -1
        self.planned_moves = []
        if Supply.TAKEOVER in self.supplies:
            rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
            self.planned_moves = [str(self.supplies.index(Supply.TAKEOVER)), choice(rivals_idx)]
        elif self.summons_amount > 0 and not self.zombie_in_city:
            self.play_summons()
        elif self.summons_amount > 0 and (self.zombie_in_city and not self.game_state.final_attack)\
                and self.zombie_amount == 0:
            self.change_city_state()
        elif self.defences_amount > 0 and (self.obstacle_amount < 3 or self.zombie_amount > 2):
            self.play_defences()
        elif self.zombie_amount > 0:
            self.defend_policy()
        elif not self.zombie_in_city:
            self.change_city_state()
        elif self.zombie_in_city and not self.game_state.final_attack:
            self.play_aggressively()

    def play_aggressively(self):
        if Supply.LURE_OUT in self.supplies:
            self.use_lure_out()
        elif Supply.SWAP in self.supplies and self.counters_amount + self.weapons_amount > 1:
            self.use_swap()
        elif Supply.CHAINSAW in self.supplies and self.counters_amount + self.weapons_amount > 1:
            self.use_chainsaw()

    def change_city_state(self):
        if Supply.SNIPER in self.supplies and self.zombie_in_city:
            self.use_sniper()
        elif Supply.LURE_OUT in self.supplies and self.zombie_in_city:
            self.use_lure_out()
        elif True in self.supplies_loud and self.weapons_amount + self.counters_amount > 1:
            self.play_card_for_noise()
        elif True in self.supplies_loud and self.summons_amount > 1:
            self.play_card_for_noise()

    def play_card_for_noise(self):
        tmp = copy(self.supplies)
        if Supply.MEGAPHONE in self.supplies:
            tmp.pop(tmp.index(Supply.MEGAPHONE))
            tmp.append(Supply.MEGAPHONE)
        if Supply.FLARE_GUN in self.supplies:
            tmp.pop(tmp.index(Supply.FLARE_GUN))
            tmp.append(Supply.FLARE_GUN)
        tmp_loud = [common.is_loud(supply) for supply in tmp]
        obj = tmp[tmp_loud.index(True)]
        if obj not in [Supply.SWAP, Supply.CHAINSAW]:
            index = self.supplies.index(obj)
            self.planned_moves = [str(index)]
        elif obj == Supply.SWAP:
            self.use_swap()
        else:
            self.use_chainsaw()

    def play_summons(self):
        if Supply.RADIO in self.supplies and not self.zombie_in_city:
            self.planned_moves = [str(self.supplies.index(Supply.RADIO))]
        elif Supply.FLARE_GUN in self.supplies:
            self.planned_moves = [str(self.supplies.index(Supply.FLARE_GUN))]
        elif Supply.MEGAPHONE in self.supplies:
            self.planned_moves = [str(self.supplies.index(Supply.MEGAPHONE))]

    def play_defences(self):
        self.planned_moves = [str(self.supplies_types.index(SupplyType.DEFENCE))]

    def defend_policy(self):
        if self.weapons_amount > 0:
            self.defend_with_weapon()

        if self.counters_amount > 0:
            self.defend_with_counter()

    def defend_with_weapon(self):
        big_zombie, lesser_count = common.count_zombies(self.game_state)
        if Supply.AXE in self.supplies and lesser_count > 0:
            self.planned_moves = [str(self.supplies.index(Supply.AXE))]
        elif Supply.GUN in self.supplies and lesser_count > 0:
            self.planned_moves = [str(self.supplies.index(Supply.GUN))]
        elif Supply.SHOTGUN in self.supplies:
            self.use_shotgun()
        elif Supply.SNIPER in self.supplies:
            self.use_sniper(defend=True)

    def defend_with_counter(self):
        if Supply.SWAP in self.supplies:
            self.use_swap()
        elif Supply.DRONE in self.supplies:
            self.use_drone()
        elif Supply.LURE_OUT in self.supplies:
            self.use_lure_out()
        elif Supply.SACRIFICE in self.supplies and self.zombie_amount > 1:
            self.use_sacrifice()

    def defend_with_mine_field(self):
        if self.obstacles.count(Supply.ALARM) == 0 and self.zombie_amount > self.obstacles.count(Supply.BARRICADES):
            self.planned_moves = ['y', '0', '0']
        elif self.zombie_amount / 2 <= self.obstacles.count(Supply.MINE_FILED):
            self.planned_moves = ['y', '0', '0']
        else:
            self.planned_moves = ['n']

    def defend_with_alarm(self):
        if self.zombie_amount / 2 > self.obstacles.count(Supply.MINE_FILED) \
                and self.zombie_amount > self.obstacles.count(Supply.BARRICADES):
            self.planned_moves = ['y']
        else:
            self.planned_moves = ['n']

    def defend_with_barricades(self):
        if self.obstacles.count(Supply.ALARM) == 0 and self.obstacles.count(Supply.MINE_FILED) < self.zombie_amount / 2:
            self.planned_moves = ['y']
        else:
            self.planned_moves = ['n']

    def use_sacrifice(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        self.planned_moves = [str(self.supplies.index(Supply.SACRIFICE))]
        for _ in range(self.zombie_amount):
            self.planned_moves.append(choice(rivals_idx))

    def use_lure_out(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        big_zombie, lesser_count = common.count_zombies(self.game_state)
        self.planned_moves = [str(self.supplies.index(Supply.LURE_OUT))]
        if self.zombie_in_city:
            self.planned_moves.append('y')
            if len(rivals_idx) > 1:
                self.planned_moves.append(choice(rivals_idx))
        if big_zombie and lesser_count > 0:
            self.planned_moves.append('0')

        if len(rivals_idx) > 1:
            self.planned_moves.append(choice(rivals_idx))

    def use_drone(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        big_zombie, lesser_count = common.count_zombies(self.game_state)
        if lesser_count > 0 and big_zombie:
            self.planned_moves = \
                [str(self.supplies.index(Supply.DRONE)), choice(['0', '1']), choice(rivals_idx)]
        if lesser_count == 0 and big_zombie or not big_zombie and lesser_count > 0:
            self.planned_moves = [str(self.supplies.index(Supply.DRONE)), choice(rivals_idx)]

    def use_swap(self):
        shelters_dict = {}
        _, _, rivals = common.find_rivals_and_build_action_message(self.game_state)
        for index, shelter in enumerate(rivals):
            if shelter.name != self.name and len(shelter.zombies) == 0:
                shelters_dict[len(shelter.obstacles)] = index
        if len(shelters_dict) > 0:
            index = shelters_dict[max(shelters_dict)]
            if len(self.game_state.players[index].obstacles) >= self.obstacle_amount:
                self.planned_moves = [str(self.supplies.index(Supply.SWAP)), str(index)]

    def use_shotgun(self):
        big_zombie, lesser_count = common.count_zombies(self.game_state)
        self.planned_moves = [str(self.supplies.index(Supply.SHOTGUN))]
        if lesser_count > 1:
            self.planned_moves.append('1')
        elif big_zombie:
            self.planned_moves.append('0')

    def use_sniper(self, defend=False):
        if not self.zombie_in_city:
            self.planned_moves = [str(self.supplies.index(Supply.SNIPER)), choice(['0', '1'])]
        elif defend:
            self.planned_moves = [str(self.supplies.index(Supply.SNIPER)), 'n', choice(['0', '1'])]
        else:
            self.planned_moves = [str(self.supplies.index(Supply.SNIPER)), 'y']

    def use_chainsaw(self):
        shelters_dict = {}
        rivals = []
        for rival in self.game_state.players:
            if rival.name != self.name and not rival.defeated and len(rival.obstacles) > 0:
                rivals.append(rival)
        for index, shelter in enumerate(rivals):
            if len(shelter.zombies) == 0:
                shelters_dict[len(shelter.obstacles)] = index
        if len(shelters_dict) > 0:
            index = shelters_dict[max(shelters_dict)]
            self.planned_moves = [str(self.supplies.index(Supply.CHAINSAW)), str(index)]
        else:
            self.planned_moves = [str(self.supplies.index(Supply.CHAINSAW)), '0']
