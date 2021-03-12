def singleton(cls):
    instances = {}

    def getinstance(*a, **kw):
        if cls not in instances:
            instances[cls] = cls(*a, **kw)
        return instances[cls]

    return getinstance


@singleton
class Capital:
    def __init__(self, city_name):
        self.__name = city_name

    def name(self):
        return self.__name


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing

    ukraine_capital_1 = Capital("Kyiv")
    ukraine_capital_2 = Capital("London")
    ukraine_capital_3 = Capital("Marocco")

    assert ukraine_capital_2.name() == "Kyiv"
    assert ukraine_capital_3.name() == "Kyiv"

    assert ukraine_capital_2 is ukraine_capital_1
    assert ukraine_capital_3 is ukraine_capital_1

    print("Coding complete? Let's try tests!")
