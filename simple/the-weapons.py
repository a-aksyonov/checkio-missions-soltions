from enum import Enum

MY_DEBUG = False


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


def more_or_zero(*args):
    """Sums arguments and return their sum
        if it greater than zero and zero otherwise.
    """
    result = sum(args)
    return result if result > 0 else 0


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


def fight(unit_1, unit_2, fight_type=FightType.DUEL):
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.do_attack(unit_2, fight_type)
        if unit_2.is_alive:
            unit_2.do_attack(unit_1, fight_type)
    return unit_1.is_alive


class Army:
    def __init__(self):
        self.units = list()

    def add_units(self, warrior_class, num: int):
        if num > 0:
            self.units.extend([warrior_class() for i in range(num)])
            self.refresh_stack()

    def remove_deads(self):
        for idx in range(len(self.units) - 1, -1, -1):
            if not self.units[idx].is_alive:
                del self.units[idx]
        self.refresh_stack()

    def refresh_stack(self):
        for idx, unit in enumerate(self.units[:-1]):
            unit.unit_behind = self.units[idx + 1]
        try:
            self.units[-1].unit_behind = None
        except IndexError:
            pass

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
        while army1 and army2:
            fight(army1.get_front_fighter(), army2.get_front_fighter(),
                  FightType.STACK)
            army1.remove_deads()
            army2.remove_deads()
        return army1.is_alive

    def straight_fight(self, army1: Army, army2: Army):
        print_armies("Before straight fight", army1, army2)
        while army1 and army2:
            for unit1, unit2 in zip(army1.units, army2.units):
                fight(unit1, unit2)
            print_armies("Inside straight fight", army1, army2)
            army1.remove_deads()
            army2.remove_deads()
            print_armies("After cleanup straight fight", army1, army2)
        print_armies("After straight fight", army1, army2)
        return army1.is_alive


if __name__ == "__main__":
    # These "asserts" using only for self-checking and not necessary for auto-testing

    ogre = Warrior()
    lancelot = Knight()
    richard = Defender()
    eric = Vampire()
    freelancer = Lancer()
    priest = Healer()

    sword = Sword()
    shield = Shield()
    axe = GreatAxe()
    katana = Katana()
    wand = MagicWand()
    super_weapon = Weapon(50, 10, 5, 150, 8)

    ogre.equip_weapon(sword)
    ogre.equip_weapon(shield)
    ogre.equip_weapon(super_weapon)
    lancelot.equip_weapon(super_weapon)
    richard.equip_weapon(shield)
    eric.equip_weapon(super_weapon)
    freelancer.equip_weapon(axe)
    freelancer.equip_weapon(katana)
    priest.equip_weapon(wand)
    priest.equip_weapon(shield)

    ogre.health == 125
    lancelot.attack == 17
    richard.defense == 4
    eric.vampirism == 200
    freelancer.health == 15
    priest.heal_power == 5

    fight(ogre, eric) == False
    fight(priest, richard) == False
    fight(lancelot, freelancer) == True

    my_army = Army()
    my_army.add_units(Knight, 1)
    my_army.add_units(Lancer, 1)

    enemy_army = Army()
    enemy_army.add_units(Vampire, 1)
    enemy_army.add_units(Healer, 1)

    my_army.units[0].equip_weapon(axe)
    my_army.units[1].equip_weapon(super_weapon)

    enemy_army.units[0].equip_weapon(katana)
    enemy_army.units[1].equip_weapon(wand)

    battle = Battle()

    battle.fight(my_army, enemy_army) == True
    print("Coding complete? Let's try tests!")
