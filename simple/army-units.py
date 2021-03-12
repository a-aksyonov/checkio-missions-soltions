from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


class Army(metaclass=ABCMeta):
    @property
    def army_name(self):
        return self.__class__.__name__[:-len('Army')]

    @abstractmethod
    def train_swordsman(self, name: str):
        pass

    @abstractmethod
    def train_lancer(self, name: str):
        pass

    @abstractmethod
    def train_archer(self, name: str):
        pass


@dataclass(init=True, repr=True, eq=True)
class Warrior:
    unit_type: str
    unit_name: str
    army_type: str

    def introduce(self):
        return f"{self.unit_type} {self.unit_name}, " + \
               f"{self.army_type} {self.__class__.__name__.lower()}"


class Swordsman(Warrior):
    pass


class Lancer(Warrior):
    pass


class Archer(Warrior):
    pass


class EuropeanArmy(Army):
    def train_swordsman(self, name: str):
        return Swordsman(unit_type='Knight',
                         unit_name=name,
                         army_type=self.army_name)

    def train_lancer(self, name: str):
        return Lancer(unit_type='Raubritter',
                      unit_name=name,
                      army_type=self.army_name)

    def train_archer(self, name: str):
        return Archer(unit_type='Ranger',
                      unit_name=name,
                      army_type=self.army_name)


class AsianArmy(Army):
    def train_swordsman(self, name: str):
        return Swordsman(unit_type='Samurai',
                         unit_name=name,
                         army_type=self.army_name)

    def train_lancer(self, name: str):
        return Lancer(unit_type='Ronin',
                      unit_name=name,
                      army_type=self.army_name)

    def train_archer(self, name: str):
        return Archer(unit_type='Shinobi',
                      unit_name=name,
                      army_type=self.army_name)


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing

    my_army = EuropeanArmy()
    enemy_army = AsianArmy()

    soldier_1 = my_army.train_swordsman("Jaks")
    soldier_2 = my_army.train_lancer("Harold")
    soldier_3 = my_army.train_archer("Robin")

    soldier_4 = enemy_army.train_swordsman("Kishimoto")
    soldier_5 = enemy_army.train_lancer("Ayabusa")
    soldier_6 = enemy_army.train_archer("Kirigae")

    assert soldier_1.introduce() == "Knight Jaks, European swordsman"
    assert soldier_2.introduce() == "Raubritter Harold, European lancer"
    assert soldier_3.introduce() == "Ranger Robin, European archer"

    assert soldier_4.introduce() == "Samurai Kishimoto, Asian swordsman"
    assert soldier_5.introduce() == "Ronin Ayabusa, Asian lancer"
    assert soldier_6.introduce() == "Shinobi Kirigae, Asian archer"

    print("Coding complete? Let's try tests!")
