def unix_match(filename: str, pattern: str) -> bool:
    import re

    def between_elder_brackets(start_from=0):
        pat_list = pattern[start_from:].split(']')
        open_idx = pattern[start_from:].find('[', start_from) + 1
        opens = 0
        for item_num, item in enumerate(pat_list):
            #print('Current:', item)
            opens += item.count('[')
            if opens:
                opens -= 1
                continue
            #print("Final:", item_num, item)
            merged_items = ']'.join(pat_list[:item_num + 1])
            close_idx = merged_items.rfind(']', start_from)
            #print("Answer = ", merged_items[open_idx:close_idx])
            return (merged_items[open_idx:close_idx])
        return None

    def all_elder_brackets():
        while True:
            start_idx = 0
            result = between_elder_brackets(start_idx)
            if result is None:
                return None
            start_idx += len(result) + 1
            yield result

    # print("Pattern", pattern)
    # between_elder_brackets()
    # exit(0)
    # escape in elder brackets
    for match_str in all_elder_brackets():
        print('match_str:', match_str)
        if match_str != '' and match_str != '!':
            if match_str[0] == '!':
                match_str_rep = '^' + re.escape(match_str[1:])
            else:
                match_str_rep = re.escape(match_str)
            pattern = pattern.replace(match_str, match_str_rep)
    pattern = pattern.replace('.', '\.')
    pattern = pattern.replace('[!]', re.escape('[!]'))
    print('pattern1:', pattern)
    pattern = re.sub(r'[^\\](?<=\*)', '.*', ' ' + pattern).strip()
    pattern = re.sub(r'[^\\](?<=\?)', '.', ' ' + pattern).strip()
    print('pattern:', pattern)
    try:
        return bool(re.match(pattern, filename))
    except re.error:
        print('except')
        return False


if __name__ == '__main__':
    print("Example:")
    print(unix_match("[?*]", "[[][?][*][]]"))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert unix_match('somefile.txt', '*') == True
    assert unix_match('other.exe', '*') == True
    assert unix_match('my.exe', '*.txt') == False
    assert unix_match('log1.txt', 'log?.txt') == True
    assert unix_match('log1.txt', 'log[1234567890].txt') == True
    assert unix_match('log12.txt', 'log?.txt') == False
    assert unix_match('log12.txt', 'log??.txt') == True
    assert unix_match("[?*]", "[[][?][*][]]") is True
    assert unix_match("apache12.log", "*[1234567890].*") is True
    assert unix_match("[!]check.txt", "[!]check.txt") is True
    assert unix_match("[check].txt", "[][]check[][].txt") is True
    print("Coding complete? Click 'Check' to earn cool rewards!")
