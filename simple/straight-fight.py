from enum import Enum

MY_DEBUG = False


class FightType(Enum):
    DUEL = 1
    STACK = 2


class Warrior:
    max_health = 50

    def __init__(self, attack=5):
        self.health = self.__class__.max_health
        self.attack = attack
        self.unit_behind = None

    def do_attack(self, whom: 'Warrior', fight_type=FightType.DUEL):
        whom.attacked(self.attack)
        self._after_attack(fight_type)

    def get_unit_behind(self):
        return self.unit_behind

    def _after_attack(self, fight_type):
        if fight_type is FightType.STACK:
            if self.get_unit_behind():
                self.get_unit_behind().heal(self)

    def attacked(self, attack):
        if attack < 0:
            attack = 0
        self.health -= attack
        return attack

    def heal(self, whom: 'Warrior'):
        pass

    def healed(self, heal_points):
        if self.health + heal_points <= self.__class__.max_health:
            self.health += heal_points
        else:
            self.health = self.__class__.max_health

    def __bool__(self):
        return self.is_alive

    def __str__(self):
        msg = f"{self.__class__.__name__}(h:{self.health})"
        return f"{msg:14}"

    __repr__ = __str__

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    max_health = 60

    def __init__(self):
        super().__init__(attack=3)
        self.defense = 2

    def attacked(self, attack):
        diff = attack - self.defense
        if diff < 0:
            diff = 0
        return super().attacked(diff)


class Rookie(Warrior):
    def __init__(self):
        super().__init__(attack=1)


class Vampire(Warrior):
    max_health = 40

    def __init__(self):
        super().__init__(attack=4)
        self.vampirism = 50

    def do_attack(self, whom: 'Warrior', fight_type=FightType.DUEL):
        self.health += int(
            round(whom.attacked(self.attack) * (self.vampirism / 100)))
        self._after_attack(fight_type)


class Lancer(Warrior):
    max_health = 50

    def __init__(self):
        super().__init__(attack=6)

    def do_attack(self, whom: 'Warrior', fight_type=FightType.DUEL):
        super().do_attack(whom, fight_type)
        if whom.get_unit_behind() and fight_type is FightType.STACK:
            whom.get_unit_behind().attacked(int(self.attack * 0.5))


class Healer(Warrior):
    max_health = 60

    def __init__(self):
        super().__init__(attack=0)
        self.heal_points = 2

    def heal(self, whom: 'Warrior'):
        if self.is_alive:
            whom.healed(self.heal_points)


def fight(unit_1, unit_2, fight_type=FightType.DUEL):
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.do_attack(unit_2, fight_type)
        if unit_2.is_alive:
            unit_2.do_attack(unit_1, fight_type)
    return unit_1.is_alive


class Army:
    def __init__(self):
        self.units_list = list()

    def add_units(self, warrior_class, num: int):
        if num > 0:
            self.units_list.extend([warrior_class() for i in range(num)])
            self.refresh_stack()

    def remove_deads(self):
        for idx in range(len(self.units_list) - 1, -1, -1):
            if not self.units_list[idx].is_alive:
                del self.units_list[idx]
        self.refresh_stack()

    def refresh_stack(self):
        for idx, unit in enumerate(self.units_list[:-1]):
            unit.unit_behind = self.units_list[idx + 1]
        try:
            self.units_list[-1].unit_behind = None
        except IndexError:
            pass

    @property
    def is_alive(self):
        return bool(self.units_list)

    def __bool__(self):
        return self.is_alive

    __nonzero__ = __bool__

    def get_front_fighter(self) -> Warrior:
        return self.units_list[0]


def print_armies(message: str, army1: 'Army', army2: 'Army'):
    if MY_DEBUG:
        print(message)
        print(army1.units_list)
        print(army2.units_list)


class Battle:
    def fight(self, army1: Army, army2: Army):
        while army1 and army2:
            fight(army1.get_front_fighter(), army2.get_front_fighter(),
                  FightType.STACK)
            army1.remove_deads()
            army2.remove_deads()
        return army1.is_alive

    def straight_fight(self, army1: Army, army2: Army):
        print_armies("Before straight fight", army1, army2)
        while army1 and army2:
            for unit1, unit2 in zip(army1.units_list, army2.units_list):
                fight(unit1, unit2)
            print_armies("Inside straight fight", army1, army2)
            army1.remove_deads()
            army2.remove_deads()
            print_armies("After cleanup straight fight", army1, army2)
        print_armies("After straight fight", army1, army2)
        return army1.is_alive


if __name__ == '__main__':
    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Lancer, 7)
    army_1.add_units(Vampire, 3)
    army_1.add_units(Healer, 1)
    army_1.add_units(Warrior, 4)
    army_1.add_units(Healer, 1)
    army_1.add_units(Defender, 2)
    army_2.add_units(Warrior, 4)
    army_2.add_units(Defender, 4)
    army_2.add_units(Healer, 1)
    army_2.add_units(Vampire, 6)
    army_2.add_units(Lancer, 4)
    battle = Battle()
    assert not battle.straight_fight(army_1, army_2)

if __name__ == '__main__':
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

if __name__ == '__main__':
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
    priest = Healer()

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
    assert freelancer.health == 14
    priest.heal(freelancer)
    assert freelancer.health == 16

    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 4)
    enemy_army.add_units(Healer, 1)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)
    enemy_army.add_units(Healer, 1)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Healer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Healer, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True
    print("Coding complete? Let's try tests!")

if __name__ == '__main__':
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
    priest = Healer()

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
    assert freelancer.health == 14
    priest.heal(freelancer)
    assert freelancer.health == 16

    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 4)
    enemy_army.add_units(Healer, 1)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)
    enemy_army.add_units(Healer, 1)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Healer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Healer, 1)
    army_4.add_units(Lancer, 2)

    army_5 = Army()
    army_5.add_units(Warrior, 10)

    army_6 = Army()
    army_6.add_units(Warrior, 6)
    army_6.add_units(Lancer, 5)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True
    assert battle.straight_fight(army_5, army_6) == False
    print("Coding complete? Let's try tests!")