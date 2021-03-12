MY_DEBUG = True


class Warrior:
    def __init__(self, health=50, attack=5):
        self.health = health
        self.attack = attack

    def do_attack(self, whom: 'Warrior'):
        whom.attacked(self.attack)

    def attack_army(self, enemy_army: 'Army'):
        self.do_attack(enemy_army.get_fighter())

    def attacked(self, attack):
        if attack < 0:
            attack = 0
        self.health -= attack
        return attack

    def get_damage_list(self):
        return [self.attack]

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


class Rookie(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=1)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50

    def do_attack(self, whom: 'Warrior'):
        self.health += int(
            round(whom.attacked(self.attack) * (self.vampirism / 100)))


class Lancer(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=6)

    def attack_army(self, enemy_army: 'Army'):
        super().attack_army(enemy_army)
        if len(enemy_army.units_list) > 1:
            enemy_army.units_list[1].attacked(int(self.attack * 0.5))


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

    def remove_deads(self):
        for idx in range(len(self.units_list) - 1, -1, -1):
            if not self.units_list[idx].is_alive:
                del self.units_list[idx]

    @property
    def is_alive(self):
        return bool(self.units_list)

    def __bool__(self):
        return self.is_alive

    __nonzero__ = __bool__

    def get_fighter(self) -> Warrior:
        return self.units_list[0]


def fight_with_army(army_1: 'Army', army_2: 'Army'):
    unit_1 = army_1.get_fighter()
    unit_2 = army_2.get_fighter()
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.attack_army(army_2)
        if unit_2.is_alive:
            unit_2.attack_army(army_1)
    return unit_1.is_alive


def print_armies(message: str, army1: 'Army', army2: 'Army'):
    if MY_DEBUG:
        print(message)
        print(army1.units_list)
        print(army2.units_list)


class Battle:
    def fight(self, army1: Army, army2: Army):
        while army1 and army2:
            fight_with_army(army1, army2)
            army1.remove_deads()
            army2.remove_deads()
        return army1.is_alive


if __name__ == '__main__':
    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Defender, 11)
    army_1.add_units(Vampire, 3)
    army_1.add_units(Warrior, 4)
    army_2.add_units(Warrior, 4)
    army_2.add_units(Defender, 4)
    army_2.add_units(Vampire, 13)
    battle = Battle()
    assert battle.fight(army_1, army_2)

if __name__ == '__main__':
    # fight tests
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
    freelancer = Lancer()
    vampire = Vampire()

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
    assert fight(freelancer, vampire) == True
    assert freelancer.is_alive == True

    #battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 4)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
    assert battle.fight(army_3, army_4) == False
    print("Coding complete? Let's try tests!")