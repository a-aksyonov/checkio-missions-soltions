import re
VOWELS = "aeiouy"


def translate1(phrase):
    listn = []
    for word in phrase.split():
        listn.append(re.sub('([^aeiouy])[aeiouy]', r'\1', word))

    return re.sub('([aeiouy]){3}', r'\1', ' '.join(listn))


def translate(phrase):
    return re.sub('([aeiouy]){3}', r'\1',
                  re.sub(r'([^aeiouy\s])[aeiouy]', r'\1', phrase))


if __name__ == '__main__':
    print("Example:")
    print(translate("hieeelalaooo"))

    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert translate("hieeelalaooo") == "hello", "Hi!"
    assert translate("hoooowe yyyooouuu duoooiiine") == "how you doin", "Joey?"
    assert translate("aaa bo cy da eee fe") == "a b c d e f", "Alphabet"
    assert translate("sooooso aaaaaaaaa") == "sos aaa", "Mayday, mayday"
    print(
        "Coding complete? Click 'Check' to review your tests and earn cool rewards!"
    )
