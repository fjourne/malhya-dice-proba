import operator
import collections



from dice import *
from roll_constant import *


def dict_add(key, dicti, value):
    dicti[key] = (dicti[key] if key in dicti else 0) + value


def level_fail(success: int, fail: int) -> (int, int):
    f = fail
    s = success
    if fail >= comp_fail_at:
        f = comp_fail_at
        s = 0
    return s, f


def roll_comb() -> dict[int, float]:
    cummul_damage = {(comb_flat, 0, 0, 0): 1.0}
    r_roll = de(comb_nb_r, comb_r)
    y_roll = de(comb_nb_y, comb_y)

    cummul_damage = comb_cummul(cummul_damage, r_roll)
    cummul_damage = comb_cummul(cummul_damage, y_roll)

    result = {}
    for (damage_roll, p_a) in cummul_damage.items():
        damage, shield_red, blue_dice_red, black_dice_red = damage_roll
        cummul_defense = {comb_def_empty: 1.0}
        nb_blue = comb_nb_blue - blue_dice_red
        nb_black = comb_nb_black - black_dice_red
        if nb_blue > 0:
            blue_roll = de(nb_blue, comb_blue)
            cummul_defense = comb_cummul(cummul_defense, blue_roll)
        if nb_black > 0:
            black_roll = de(nb_black, comb_black)
            cummul_defense = comb_cummul(cummul_defense, black_roll)
        for (defence_roll, p_d) in cummul_defense.items():
            damage_red, cancel = defence_roll
            damage = 0 if cancel > 0 else max((damage - max(0, damage_red - shield_red)), 0)
            dict_add(damage, result, p_a * p_d)
    return collections.OrderedDict(sorted(result.items()))


def comb_cummul(result: dict[tuple[int, ...], float], roll: dict[tuple[int, ...], float]) -> dict[tuple[int, ...], float]:
    cummul = {}
    for d_c, pc in result.items():
        for d_r, pr in roll.items():
            dict_add(tuple(map(operator.add, d_c, d_r)), cummul, pc * pr)
    return cummul


def roll_comp() -> dict[int, float]:
    roll = {}
    w_roll = de(comp_nb_w, comp_w)
    b_roll = de(comp_nb_b, comp_b)
    for success, p1 in w_roll.items():
        for fail, p2 in b_roll.items():
            s, f = level_fail(success[0], fail[0])
            dict_add((s, f), roll, p1 * p2)

    rolls = roll_comp_aux(roll, {(0, 0): 1.0}, comp_max_roll)

    result = {}
    for (success, fail), p in rolls.items():
        dict_add(success, result, p)
    return result


def roll_comp_aux(roll: dict[(int, int), float], current: dict[(int, int), float], roll_left:int) -> dict[(int, int), float]:
    if roll_left == 0:
        return current

    cummul = {}

    for (s1, f1), p1 in current.items():
        if f1 + comp_margin >= comp_fail_at or s1 >= comp_stop_at:
            success = s1
            fail = f1
            p = p1
            dict_add((success, fail), cummul, p)
        else:
            for (s2, f2), p2 in roll.items():
                success, fail = level_fail(s1 + s2, f1 + f2)
                p = p1*p2
                dict_add((success, fail), cummul, p)
    return roll_comp_aux(roll, cummul, roll_left - 1)


def de(nb_die: int, die: list) -> dict[tuple[int, ...], float]:
    dice = die.copy()
    dice_proba = compute_dice_probabilities(dice)
    dice_effect_nb = len(die[0])
    result = {(0,) * dice_effect_nb: 1.0}
    for i in range(0, nb_die):
        new_result = {}
        for r1, p1 in result.items():
            for r2, p2 in dice_proba.items():
                r = tuple(map(operator.add, r1, r2))
                dict_add(r, new_result, p1*p2)
        result = new_result
    return result


def compute_dice_probabilities(result: list[list[int]]) -> dict[list[int], float]:
    proba = {}
    result_read = 0
    nb_face = len(result)
    for i in range(0, nb_face):
        dict_add(result[i], proba, 1.0 / nb_face)
    return proba


def display_proba(proba: dict):
    print("Roll : ")
    for r, p in proba.items():
        print_bar(r, p)


def display_at_least(proba: dict):
    print("At Least : ")
    at_leat = 1.0
    for r, p in proba.items():
        print_bar(r, at_leat)
        at_leat -= p


def print_bar(v: int, p: float):
    p = p * 100
    prefix_v = ' ' if v < 10 else ''
    prefix_p = '  ' if p < 10 else ' ' if p < 100 else ''
    bar = "x" * int(p * 2)
    if p > 0.01:
        print('{}{}: {}{:.2f}%  {}'.format(prefix_v, v, prefix_p, p, bar))


def compute_average(proba: dict[int, float]) -> float:
    average = 0
    for success, p in proba.items():
        average += success*p
    return average