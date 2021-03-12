def isometric_strings(str1: str, str2: str) -> bool:
    def convert(str_from: str, rule_map: dict) -> str:
        return ''.join([rule_map.get(char) for char in str_from])

    return convert(str1, dict(zip(str1, str2))) == str2 and convert(
        str2, dict(zip(str2, str1))) == str1


if __name__ == '__main__':
    print("Example:")
    print(isometric_strings('add', 'egg'))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert isometric_strings('add', 'egg') == True
    assert isometric_strings('foo', 'bar') == False
    assert isometric_strings('', '') == True
    assert isometric_strings('all', 'all') == True
    print("Coding complete? Click 'Check' to earn cool rewards!")
