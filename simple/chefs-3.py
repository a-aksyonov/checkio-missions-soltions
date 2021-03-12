from abc import ABCMeta, abstractmethod


class AbstractCook(metaclass=ABCMeta):
    meal_name = None
    drink_name = None

    @abstractmethod
    def add_food(self, amount, price):
        pass

    @abstractmethod
    def add_drink(self, amount, price):
        pass

    @abstractmethod
    def total(self):
        pass


class Cheff(AbstractCook):
    def __init__(self):
        self.meal_price = 0
        self.drink_price = 0

    def add_food(self, amount, price):
        self.meal_price += price * amount

    def add_drink(self, amount, price):
        self.drink_price += price * amount

    def total(self):
        return "{}: {}, {}: {}, Total: {}".format(
            self.meal_name, self.meal_price, self.drink_name, self.drink_price,
            self.meal_price + self.drink_price)


class JapaneseCook(Cheff):
    meal_name = "Sushi"
    drink_name = "Tea"


class RussianCook(Cheff):
    meal_name = "Dumplings"
    drink_name = "Compote"


class ItalianCook(Cheff):
    meal_name = "Pizza"
    drink_name = "Juice"


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing

    client_1 = JapaneseCook()
    client_1.add_food(2, 30)
    client_1.add_food(3, 15)
    client_1.add_drink(2, 10)

    client_2 = RussianCook()
    client_2.add_food(1, 40)
    client_2.add_food(2, 25)
    client_2.add_drink(5, 20)

    client_3 = ItalianCook()
    client_3.add_food(2, 20)
    client_3.add_food(2, 30)
    client_3.add_drink(2, 10)

    assert client_1.total() == "Sushi: 105, Tea: 20, Total: 125"
    assert client_2.total() == "Dumplings: 90, Compote: 100, Total: 190"
    assert client_3.total() == "Pizza: 100, Juice: 20, Total: 120"
    print("Coding complete? Let's try tests!")
