from zombie_enums import ZombieType
from supply_enums import Supply, SupplyType
from player_shelter import PlayerShelter
import common_logic


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

    def cpu_input(self, _message):
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
        for key in self.policy:
            self.policy[key] = False
        self.discard_and_counter_summons_policies()

        if self.zombie_amount > 0:
            self.defend_policy()

        self.end_turn_policy()
        self.print('Test')

    def defend_policy(self):
        if self.weapons_amount > 0:
            self.planned_moves = [(self.supplies_types.index(SupplyType.WEAPON))]

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
