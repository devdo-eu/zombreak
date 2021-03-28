

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
        self.gui = lambda x: ''
