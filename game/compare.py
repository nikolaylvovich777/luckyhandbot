#  -*- coding: utf-8 -*-
STONE = 'a'  # 'stone'
SCISSORS = 'c'  # 'scissors'
PAPER = 'b'  # 'paper'


def compare(a, b):
    if a == STONE and b == SCISSORS:
        return 1
    elif a == STONE and b == PAPER:
        return 2
    elif a == SCISSORS and b == STONE:
        return 2
    elif a == SCISSORS and b == PAPER:
        return 1
    elif a == PAPER and b == STONE:
        return 1
    elif a == PAPER and b == SCISSORS:
        return 2
    assert a == b
    return -1
