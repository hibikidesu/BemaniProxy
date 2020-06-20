from enum import Enum
from math import floor


class Grade(Enum):
    NO_PLAY = 0
    D = 1
    C = 2
    B = 3
    A = 4
    A_PLUS = 5
    AA = 6
    AA_PLUS = 7
    AAA = 8
    AAA_PLUS = 9
    S = 10


class ClearType(Enum):
    NO_PLAY = 0
    FAILED = 1
    CLEAR = 2
    HARD_CLEAR = 3
    ULTIMATE_CHAIN = 4
    PERFECT_ULTIMATE_CHAIN = 5


def find_grade(score: int) -> Grade:
    if score >= 9900000:
        return Grade.S
    elif score >= 9800000:
        return Grade.AAA_PLUS
    elif score >= 9700000:
        return Grade.AAA
    elif score >= 9500000:
        return Grade.AA_PLUS
    elif score >= 9300000:
        return Grade.AA
    elif score >= 9000000:
        return Grade.A_PLUS
    elif score >= 8700000:
        return Grade.A
    elif score >= 7500000:
        return Grade.B
    elif score >= 8500000:
        return Grade.C
    return Grade.D


def calculate_volforce(score: int, level: int, grade: Grade, clear: ClearType) -> float:
    pass
