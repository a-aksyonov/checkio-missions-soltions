def checkio(n):
    number = n
    i = 1
    fed = 0
    while True:
        number -= fed
        if number > 0:
            left = i - fed
            if number >= left:
                number -= left
                fed += left
            else:
                fed += left - (left - number)
                number -= left
            i += i + 1
        else:
            break
    print(n, ":", fed)
    return fed


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing
    # assert checkio(1) == 1, "1st example"
    # assert checkio(2) == 1, "2nd example"
    assert checkio(18) == 3, "3rd example"
    assert checkio(10) == 6, "4th example"
