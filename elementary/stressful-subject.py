from collections import OrderedDict
import itertools
import re


def is_stressful(subj):
    """
        recognize stressful subject
    """
    if subj[-3:] == '!!!' or subj.isupper():
        return True
    dl = [
        OrderedDict.fromkeys('help'),
        OrderedDict.fromkeys('asap'),
        OrderedDict.fromkeys('urgent')
    ]
    wds = [''.join(d.keys()) for d in dl]
    wds = ["help", "asap", "urgent"]
    return bool(
        re.search(
            f'({"|".join(wds)})', ''.join(ch for ch, _ in itertools.groupby(
                re.sub(r'[^A-Za-z]+', "", subj).lower()))))


if __name__ == '__main__':
    # These "asserts" are only for self-checking
    # and not necessarily for auto-testing
    assert is_stressful("Hi") == False, "First"
    assert is_stressful("I neeed HELP") == True, "Second"
    assert is_stressful("We need you A.S.A.P.!!") == True
    print('Done! Go Check it!')
