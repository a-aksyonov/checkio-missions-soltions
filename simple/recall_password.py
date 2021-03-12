from typing import List


def recall_password(grille: List[str], password: List[str]) -> str:
    import itertools
    result = ''
    for (g_y, g_x) in itertools.product(range(4), range(4)):
        print(grille[g_y][g_x], password[g_x][g_y], end='; ')
        if grille[g_y][g_x] == 'X':
            result += password[g_y][g_x]
    print()
    for (g_x, g_y), (p_x,
                     p_y) in zip(itertools.product(range(4), range(3, -1, -1)),
                                 itertools.product(range(4), range(4))):
        print(grille[g_y][g_x], password[p_y][p_x], end='; ')
        if grille[g_y][g_x] == 'X':
            result += password[p_x][p_y]
    print()
    for (g_x, g_y), (p_x, p_y) in zip(
            itertools.product(range(3, -1, -1), range(3, -1, -1)),
            itertools.product(range(4), range(4))):
        print(grille[g_x][g_y], password[p_x][p_y], end='; ')
        if grille[g_x][g_y] == 'X':
            result += password[p_x][p_y]
    print()
    for (g_x, g_y), (p_x,
                     p_y) in zip(itertools.product(range(3, -1, -1), range(4)),
                                 itertools.product(range(4), range(4))):
        print(grille[g_y][g_x], password[p_x][p_y], end='; ')
        if grille[g_y][g_x] == 'X':
            result += password[p_x][p_y]
    print()
    return result


if __name__ == '__main__':
    print("Example:")
    print(
        recall_password(['X...', '..X.', 'X..X', '....'],
                        ['itdf', 'gdce', 'aton', 'qrdi']))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert recall_password(
        ['X...', '..X.', 'X..X', '....'],
        ['itdf', 'gdce', 'aton', 'qrdi']) == 'icantforgetiddqd'
    assert recall_password(
        ['....', 'X..X', '.X..', '...X'],
        ['xhwc', 'rsqx', 'xqzz', 'fyzr']) == 'rxqrwsfzxqxzhczy'
    print("Coding complete? Click 'Check' to earn cool rewards!")
