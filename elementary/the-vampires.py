class Warrior:
    def __init__(self, health=50, attack=5):
        self.health = health
        self.attack = attack

    def do_attack(self, whom: 'Warrior'):
        whom.attacked(self.attack)

    def attacked(self, attack):
        self.health -= attack
        return attack

    def __str__(self):
        return f"{self.__class__.__name__}_{self.health}"

    __repr__ = __str__

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self.defense = 2

    def attacked(self, attack):
        diff = attack - self.defense
        if diff < 0:
            diff = 0
        return super().attacked(diff)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50

    def do_attack(self, whom: 'Warrior'):
        self.health += int(
            round(whom.attacked(self.attack) * (self.vampirism / 100)))


def fight(unit_1, unit_2):
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.do_attack(unit_2)
        if unit_2.is_alive:
            unit_2.do_attack(unit_1)
    return unit_1.is_alive


class Army:
    def __init__(self):
        self.units_list = list()

    def add_units(self, warrior_class, num: int):
        if num > 0:
            self.units_list.extend([warrior_class() for i in range(num)])

    @property
    def is_alive(self):
        return bool(self.units_list)

    def __bool__(self):
        return self.is_alive

    __nonzero__ = __bool__

    def refresh(self):
        if not self.get_fighter().is_alive:
            del self.units_list[0]

    def get_fighter(self) -> Warrior:
        return self.units_list[0]


class Battle:
    def fight(self, army1: Army, army2: Army):
        while army1 and army2:
            fight(army1.get_fighter(), army2.get_fighter())
            army1.refresh()
            army2.refresh()
        return army1.is_alive


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing

    #fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()

    assert fight(eric, richard) == False
    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
    assert fight(bob, mike) == False
    assert fight(lancelot, rog) == True
    assert fight(eric, richard) == False
    assert fight(ogre, adam) == True

    #battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Defender, 4)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True
    print("Coding complete? Let's try tests!")