from enum import Enum

MY_DEBUG = True


class Weapon:
    def __init__(self,
                 health=0,
                 attack=0,
                 defense=0,
                 vampirism=0,
                 heal_power=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism
        self.heal_power = heal_power


class Sword(Weapon):
    def __init__(self):
        super().__init__(health=5, attack=2)


class Shield(Weapon):
    def __init__(self):
        super().__init__(health=20, attack=-1, defense=2)


class GreatAxe(Weapon):
    def __init__(self):
        super().__init__(health=-15, attack=5, defense=-2, vampirism=10)


class Katana(Weapon):
    def __init__(self):
        super().__init__(health=-20, attack=6, defense=-5, vampirism=50)


class MagicWand(Weapon):
    def __init__(self):
        super().__init__(health=30, attack=3, heal_power=3)


class FightType(Enum):
    DUEL = 1
    STACK = 2


def more_or_zero(what: int, increment: int):
    return what + increment if what + increment > 0 else 0


class Warrior:
    base_max_health = 50

    def __init__(self, attack=5):
        self.max_health = self.__class__.base_max_health
        self.health = self.max_health
        self.attack = attack
        self.unit_behind = None
        self.weapon = None

    def do_attack(self, whom: "Warrior", fight_type=FightType.DUEL):
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

    def heal(self, whom: "Warrior"):
        pass

    def healed(self, heal_points):
        if self.health + heal_points <= self.max_health:
            self.health += heal_points
        else:
            self.health = self.max_health

    def equip_weapon(self, weapon_name: 'Weapon'):
        self.weapon = weapon_name
        self.max_health = more_or_zero(self.max_health, weapon_name.health)
        self.health = more_or_zero(self.health, weapon_name.health)
        self.attack = more_or_zero(self.attack, weapon_name.attack)

    def __bool__(self):
        return self.is_alive

    def __str__(self):
        msg = f"{self.__class__.__name__}(h{self.health};a{self.attack})"
        return f"{msg:14}"

    __repr__ = __str__

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    base_max_health = 60

    def __init__(self):
        super().__init__(attack=3)
        self.defense = 2

    def attacked(self, attack):
        diff = attack - self.defense
        if diff < 0:
            diff = 0
        return super().attacked(diff)

    def equip_weapon(self, weapon_name: 'Weapon'):
        super().equip_weapon(weapon_name)
        self.defense = more_or_zero(self.defense, weapon_name.defense)

    def __str__(self):
        msg = super().__str__()
        msg = f"{msg[:-1]};d{self.defense})"
        return f"{msg:14}"

    __repr__ = __str__


class Rookie(Warrior):
    def __init__(self):
        super().__init__(attack=1)


class Vampire(Warrior):
    base_max_health = 40

    def __init__(self):
        super().__init__(attack=4)
        self.vampirism = 50

    def do_attack(self, whom: "Warrior", fight_type=FightType.DUEL):
        self.health += int(
            round(whom.attacked(self.attack) * (self.vampirism / 100)))
        self._after_attack(fight_type)

    def equip_weapon(self, weapon_name: 'Weapon'):
        super().equip_weapon(weapon_name)
        self.vampirism = more_or_zero(self.vampirism, weapon_name.vampirism)


class Lancer(Warrior):
    base_max_health = 50

    def __init__(self):
        super().__init__(attack=6)

    def do_attack(self, whom: "Warrior", fight_type=FightType.DUEL):
        super().do_attack(whom, fight_type)
        if whom.get_unit_behind() and fight_type is FightType.STACK:
            whom.get_unit_behind().attacked(int(self.attack * 0.5))


class Healer(Warrior):
    base_max_health = 60

    def __init__(self):
        super().__init__(attack=0)
        self.heal_power = 2

    def heal(self, whom: "Warrior"):
        if self.is_alive:
            whom.healed(self.heal_power)

    def equip_weapon(self, weapon_name: 'Weapon'):
        super().equip_weapon(weapon_name)
        self.heal_power = more_or_zero(self.heal_power, weapon_name.heal_power)


class Warlord(Defender):
    base_max_health = 100

    def __init__(self):
        super().__init__()
        self.attack = 4
        self.defense = 2


def fight(unit_1, unit_2, fight_type=FightType.DUEL):
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.do_attack(unit_2, fight_type)
        if unit_2.is_alive:
            unit_2.do_attack(unit_1, fight_type)
    return unit_1.is_alive


class Army:
    def __init__(self):
        self.units = list()

    @property
    def warlord(self):
        return any(isinstance(x, Warlord) for x in self.units)

    def add_units(self, warrior_class, num: int):
        if warrior_class is Warlord:
            if self.warlord:
                return
            else:
                self.units.append(Warlord())
                return
        if num > 0:
            self.units.extend([warrior_class() for i in range(num)])

    def remove_deads(self, refresh=True):
        for idx in range(len(self.units) - 1, -1, -1):
            if not self.units[idx].is_alive:
                del self.units[idx]
        if refresh:
            self.refresh_stack()

    def refresh_stack(self):
        self.move_units()
        for idx, unit in enumerate(self.units[:-1]):
            unit.unit_behind = self.units[idx + 1]
        try:
            self.units[-1].unit_behind = None
        except IndexError:
            pass

    def pop_unit(self, *warrior_classes, ignore=False):
        for idx, unit in enumerate(self.units):
            if ignore != (unit.__class__.__name__ in map(
                    lambda x: x.__name__, warrior_classes)):
                return self.units.pop(idx)
        return None

    def move_units(self):
        """Find lancers
        Find Healers
        Find other Warriors
        """
        if not self.warlord:
            return
        front_unit = self.pop_unit(Lancer)
        if not front_unit:
            front_unit = self.pop_unit(Lancer, Healer, Warlord, ignore=True)
        if not front_unit:
            front_unit = self.pop_unit(Healer)
        if not front_unit:
            front_unit = self.pop_unit(Warlord)
        healers_and_lancers = list()
        for class_name in (Healer, Lancer):
            curr_unit = self.pop_unit(class_name)
            while curr_unit:
                healers_and_lancers.append(curr_unit)
                curr_unit = self.pop_unit(class_name)
        war_lord = self.pop_unit(Warlord)
        self.units = [front_unit] + healers_and_lancers + self.units
        if war_lord:
            self.units.append(war_lord)

    @property
    def is_alive(self):
        return bool(self.units)

    def __bool__(self):
        return self.is_alive

    __nonzero__ = __bool__

    def get_front_fighter(self) -> Warrior:
        return self.units[0]


def print_armies(message: str, army1: "Army", army2: "Army"):
    if MY_DEBUG:
        print(message)
        print(army1.units)
        print(army2.units)


class Battle:
    def fight(self, army1: Army, army2: Army):
        army1.refresh_stack()
        army2.refresh_stack()
        print_armies("Before fight", army1, army2)
        while army1 and army2:
            fight(army1.get_front_fighter(), army2.get_front_fighter(),
                  FightType.STACK)
            print_armies("Inside fight", army1, army2)
            army1.remove_deads()
            army2.remove_deads()
            print_armies("After cleanup fight", army1, army2)
        print_armies("After fight", army1, army2)
        return army1.is_alive

    def straight_fight(self, army1: Army, army2: Army):
        print_armies("Before straight fight", army1, army2)
        while army1 and army2:
            for unit1, unit2 in zip(army1.units, army2.units):
                fight(unit1, unit2)
            print_armies("Inside straight fight", army1, army2)
            army1.remove_deads(False)
            army2.remove_deads(False)
            print_armies("After cleanup straight fight", army1, army2)
        print_armies("After straight fight", army1, army2)
        return army1.is_alive


if __name__ == '__main__':
    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Warrior, 2)
    army_1.add_units(Lancer, 2)
    army_1.add_units(Defender, 1)
    army_1.add_units(Warlord, 3)
    army_2.add_units(Warlord, 2)
    army_2.add_units(Vampire, 1)
    army_2.add_units(Healer, 5)
    army_2.add_units(Knight, 2)
    army_1.move_units()
    army_2.move_units()
    battle = Battle()
    assert not battle.fight(army_1, army_2)

if __name__ == '__main__':
    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Warrior, 2)
    army_1.add_units(Lancer, 3)
    army_1.add_units(Defender, 1)
    army_1.add_units(Warlord, 1)
    army_2.add_units(Warlord, 5)
    army_2.add_units(Vampire, 1)
    army_2.add_units(Rookie, 1)
    army_2.add_units(Knight, 1)
    army_1.units[0].equip_weapon(Sword())
    army_2.units[0].equip_weapon(Shield())
    army_1.move_units()
    army_2.move_units()
    battle = Battle()
    assert not battle.straight_fight(army_1, army_2)
