from collections import namedtuple


def checkio(data):
    ArabToRome = namedtuple('ArabToRome', (1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000))
    ar2rome = ArabToRome('I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'XC', 'C', 'CD', 'D', 'CM', 'M')
    return ""


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing
    assert checkio(6) == 'VI', '6'
    assert checkio(76) == 'LXXVI', '76'
    assert checkio(499) == 'CDXCIX', '499'
    assert checkio(3888) == 'MMMDCCCLXXXVIII', '3888'
    print('Done! Go Check!')
