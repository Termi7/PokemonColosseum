import re


class Pokemon:
    """
    This is the Pokemon class with all the pokemon attributes.
    """
    def __init__(self, name='', typePokemon='', HP=0, attack=0,  defence=0, height=0, weight=0, moves=list):
        self.name=name
        self.typePokemon= typePokemon
        self.HP=HP
        self.attack=attack
        self.defence=defence
        self.height=height
        self.weight=weight
        # self.moves= moves.split(",")
        self.moves = re.split('[|,|]', moves[1:-1])

    def getName(self):
        return self.name

    def getTypePokemon(self):
        return self.typePokemon

    def getHP(self):
        return self.HP

    def getAttack(self):
        return self.attack

    def getDefence(self):
        return self.attack

    def getHeight(self):
        return self.height

    def getWeight(self):
        return self.weight

    def getMoves(self):
        return self.moves

    def setName(self, name):
        self.name = name

    def setTypePokemon(self, typePokemon):
        self.typePokemon = typePokemon

    def setHP(self, HP):
        self.HP = HP

    def setAttack(self, attack):
        self.attack = attack

    def setDefence(self, defence):
        self.defence = defence

    def setHeight(self, height):
        self.height = height

    def setWeight(self, weight):
        self.weight = weight

    def setMoves(self, moves):
        self.moves = moves










