def sun_angle(time: str):
    time_list = list(map(int, time.split(':')))
    minutes_from_rising = (time_list[0] - 6) * 60 + time_list[1]
    angle = round((minutes_from_rising / ((18 - 6) * 60)) * 180, 2)
    return angle if 0 <= angle <= 180 else "I don't see the sun!"


if __name__ == '__main__':
    print("Example:")
    print(sun_angle("07:01"))

    # These "asserts" using only for self-checking
    # and not necessary for auto-testing
    assert sun_angle("07:00") == 15
    assert sun_angle("01:23") == "I don't see the sun!"
    print("Coding complete? Click 'Check' to earn cool rewards!")
