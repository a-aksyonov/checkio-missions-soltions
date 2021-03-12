class Warrior:
    def __init__(self):
        self.health = 50
        self.damage = 5

    def attack(self, whom: 'Warrior'):
        whom.health -= self.damage

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.damage = 7


def fight(unit_1, unit_2):
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.attack(unit_2)
        if unit_2.is_alive:
            unit_2.attack(unit_1)
    return unit_1.is_alive


if __name__ == '__main__':
    #T hese "asserts" using only for self-checking
    # and not necessary for auto-testing

    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False

    print("Coding complete? Let's try tests!")
