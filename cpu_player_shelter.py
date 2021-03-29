from zombie_enums import ZombieType
from supply_enums import Supply, SupplyType
from player_shelter import PlayerShelter
import common_logic
from secrets import choice


class CPUPlayerShelter(PlayerShelter):
    def __init__(self, name='', print_foo=print):
        PlayerShelter.__init__(self, name, self.cpu_input, print_foo)
        self.gui = self.cpu_ui
        self.policy = {'discard': False, 'counter_summons': False, 'end_turn': False}
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
            return None

    @property
    def supplies_types(self):
        return [common_logic.check_type(supply) for supply in self.supplies]

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
        return [common_logic.is_loud(supply) for supply in self.supplies]

    def cpu_input(self, message):
        self.move_counter += 1
        if self.move_counter < len(self.planned_moves):
            move = self.planned_moves[self.move_counter]
        else:
            move = str(self.supply_amount)

        if '[y/n]?' in message and 'Do you want to use' in message:
            move = 'y'
        self.print(message + move)
        return move

    def cpu_ui(self, game_state):
        # self.gui_default(game_state)
        self.game_state = game_state
        self.move_counter = -1
        self.planned_moves = []
        for key in self.policy:
            self.policy[key] = False
        if Supply.TAKEOVER in self.supplies:
            rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
            self.planned_moves = [str(self.supplies.index(Supply.TAKEOVER)), choice(rivals_idx)]
        if self.zombie_amount > 0:
            self.defend_policy()
        if len(self.planned_moves) > 0:
            return
        if self.defences_amount > 0 and (self.obstacle_amount < 2 or self.zombie_amount > 2):
            self.planned_moves = [str(self.supplies_types.index(SupplyType.DEFENCE))]
        if self.summons_amount > 0:
            self.summon_policy()

        if len(self.planned_moves) > 0:
            return

        if Supply.CHAINSAW in self.supplies and not self.zombie_in_city:
            self.use_chainsaw()
            return
        self.discard_and_counter_summons_policies()
        self.end_turn_policy()

    def use_chainsaw(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        shelters_dict = {}
        for index, shelter in enumerate(self.game_state.players):
            if shelter.name != self.name and len(shelter.zombies) == 0:
                shelters_dict[len(shelter.obstacles)] = index
        index = max(shelters_dict, default=choice(rivals_idx))
        self.planned_moves = [str(self.supplies.index(Supply.CHAINSAW)), str(index)]

    def summon_policy(self):
        if not self.zombie_in_city:
            if Supply.RADIO in self.supplies:
                self.planned_moves = [str(self.supplies.index(Supply.RADIO))]
            elif Supply.FLARE_GUN in self.supplies:
                self.planned_moves = [str(self.supplies.index(Supply.FLARE_GUN))]
            elif Supply.MEGAPHONE in self.supplies:
                self.planned_moves = [str(self.supplies.index(Supply.MEGAPHONE))]

    def defend_policy(self):
        if self.weapons_amount > 0:
            self.defend_with_weapon()

        if self.counters_amount > 0:
            self.defend_with_counter()

    def defend_with_counter(self):
        if Supply.SWAP in self.supplies:
            self.use_swap()
        elif Supply.DRONE in self.supplies:
            self.use_drone()
        elif Supply.LURE_OUT in self.supplies:
            self.use_lure_out()
        elif Supply.SACRIFICE in self.supplies and self.zombie_amount > 1:
            self.use_sacrifice()

    def use_sacrifice(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        self.planned_moves = [str(self.supplies.index(Supply.SACRIFICE))]
        for _ in range(self.zombie_amount):
            self.planned_moves.append(choice(rivals_idx))

    def use_lure_out(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        big_zombie, lesser_count = common_logic.count_zombies(self.game_state)
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
        big_zombie, lesser_count = common_logic.count_zombies(self.game_state)
        if lesser_count > 0 and big_zombie:
            self.planned_moves = \
                [str(self.supplies.index(Supply.DRONE)), choice(['0', '1']), choice(rivals_idx)]
        if lesser_count == 0 and big_zombie or not big_zombie and lesser_count > 0:
            self.planned_moves = [str(self.supplies.index(Supply.DRONE)), choice(rivals_idx)]

    def use_swap(self):
        rivals_idx = [str(index) for index in range(len(self.game_state.players_still_in_game) - 1)]
        shelters_dict = {}
        for index, shelter in enumerate(self.game_state.players):
            if shelter.name != self.name and len(shelter.zombies) == 0:
                shelters_dict[len(shelter.obstacles)] = index
        index = max(shelters_dict, default=choice(rivals_idx))
        self.planned_moves = [str(self.supplies.index(Supply.SWAP)), str(index)]

    def defend_with_weapon(self):
        big_zombie, lesser_count = common_logic.count_zombies(self.game_state)
        if Supply.SHOTGUN in self.supplies:
            self.planned_moves = [str(self.supplies.index(Supply.SHOTGUN))]
            if lesser_count > 1:
                self.planned_moves.append('1')
            elif big_zombie and lesser_count > 0:
                self.planned_moves.append(choice(['0', '1']))
        elif Supply.GUN in self.supplies and lesser_count > 0 and not self.zombie_in_city:
            self.planned_moves = [str(self.supplies.index(Supply.GUN))]
        elif Supply.AXE in self.supplies and lesser_count > 0:
            self.planned_moves = [str(self.supplies.index(Supply.AXE))]
        elif Supply.SNIPER in self.supplies:
            if not self.zombie_in_city:
                self.planned_moves = [str(self.supplies.index(Supply.SNIPER)), choice(['0', '1'])]
            else:
                self.planned_moves = [str(self.supplies.index(Supply.SNIPER)), 'n', choice(['0', '1'])]

    def end_turn_policy(self):
        end_turn = True
        for policy in self.policy.values():
            if policy:
                end_turn = False
                break
        self.policy['end_turn'] = end_turn
        if self.policy['end_turn']:
            self.planned_moves = [str(self.supply_amount)]

    def discard_and_counter_summons_policies(self):
        if self.zombie_amount == 0 and self.city_amount > 3 and self.summons_amount == 0 and self.supply_amount == 3:
            self.policy['discard'] = True
            self.planned_moves = [str(len(self.supplies)), str(len(self.supplies))]

            if True in self.supplies_loud and self.weapons_amount > 1 and not self.zombie_in_city:
                self.policy['counter_summons'] = True
                self.planned_moves = [str(self.supplies_loud.index(True))]
