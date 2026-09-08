import operator
import collections


class Proba:
    # fight effect  (damage, shield remove, blue dice remove, black dice remove)
    fight_at_empty = (0, 0, 0, 0)
    fight_1d = (1, 0, 0, 0)
    fight_2d = (2, 0, 0, 0)
    fight_3d = (3, 0, 0, 0)
    # deffence effect (shield, cancel)
    fight_def_empty = (0, 0)
    fight_1s = (1, 0)
    fight_2s = (2, 0)
    fight_es = (0, 1)

    @staticmethod
    def d_skill_w(spe: int) -> list[tuple]:
        return [(0,), (0,), (1,), (1,), (1,), (spe,)]

    @staticmethod
    def d_skill_b(spe: int) -> list[tuple]:
        return [(0,), (0,), (0,), (1,), (1,), (spe,)]

    def d_fight_r(self, spe: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
        return [self.fight_1d, self.fight_2d, spe]

    def d_fight_y(self, spe: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
        return [self.fight_at_empty, self.fight_1d, self.fight_2d, self.fight_3d, self.fight_3d, spe]

    def d_fight_blue(self, spe: tuple[int, int]) -> list[tuple[int, int]]:
        return [self.fight_def_empty, self.fight_def_empty, self.fight_1s, self.fight_1s, self.fight_2s, spe]

    def d_fight_black(self, spe: tuple[int, int]) -> list[tuple[int, int]]:
        return [self.fight_def_empty, self.fight_def_empty, self.fight_def_empty, self.fight_2s, self.fight_es, spe]

    @staticmethod
    def dict_add(key, dicti, value):
        dicti[key] = (dicti[key] if key in dicti else 0) + value

    @staticmethod
    def level_fail(success: int, fail: int, skill_fail_at: int) -> (int, int):
        f = fail
        s = success
        if fail >= skill_fail_at:
            f = skill_fail_at
            s = 0
        return s, f

    def roll_fight(self, fight_flat: tuple[int, int, int, int],
                   fight_nb_r: int, fight_r: list[tuple[int, int, int, int]],
                   fight_nb_y: int, fight_y: list[tuple[int, int, int, int]],
                   fight_nb_blue: int, fight_blue: list[tuple[int, int]],
                   fight_nb_black: int, fight_black: list[tuple[int, int]]) -> dict[int, float]:
        cummul_damage = {fight_flat: 1.0}
        r_roll = self.de(fight_nb_r, fight_r)
        y_roll = self.de(fight_nb_y, fight_y)
        cummul_damage = self.fight_cummul(cummul_damage, r_roll)
        cummul_damage = self.fight_cummul(cummul_damage, y_roll)

        result = {}
        for (damage_roll, p_a) in cummul_damage.items():
            damage, shield_red, blue_dice_red, black_dice_red = damage_roll
            cummul_defense = {self.fight_def_empty: 1.0}
            nb_blue = fight_nb_blue - blue_dice_red
            nb_black = fight_nb_black - black_dice_red
            if nb_blue > 0:
                blue_roll = self.de(nb_blue, fight_blue)
                cummul_defense = self.fight_cummul(cummul_defense, blue_roll)
            if nb_black > 0:
                black_roll = self.de(nb_black, fight_black)
                cummul_defense = self.fight_cummul(cummul_defense, black_roll)
            for (defence_roll, p_d) in cummul_defense.items():
                damage_red, cancel = defence_roll
                total_damage = 0 if cancel > 0 else max((damage - max(0, damage_red - shield_red)), 0)
                self.dict_add(total_damage, result, p_a * p_d)
        return collections.OrderedDict(sorted(result.items()))

    def fight_cummul(self, result: dict[tuple[int, ...], float], roll: dict[tuple[int, ...], float]) -> \
            dict[tuple[int, ...], float]:
        cummul = {}
        for d_c, pc in result.items():
            for d_r, pr in roll.items():
                self.dict_add(tuple(map(operator.add, d_c, d_r)), cummul, pc * pr)
        return cummul

    def roll_skill(self, skill_nb_w: int, skill_w: list[tuple[int]],
                   skill_nb_b: int, skill_b: list[tuple[int]],
                   skill_max_roll: int,
                   skill_margin: int,
                   skill_fail_at: int,
                   skill_continue_under: int,
                   skill_stop_at: int) -> dict[int, float]:
        roll = {}
        w_roll = self.de(skill_nb_w, skill_w)
        b_roll = self.de(skill_nb_b, skill_b)
        for success, p1 in w_roll.items():
            for fail, p2 in b_roll.items():
                s, f = self.level_fail(success[0], fail[0], skill_fail_at)
                self.dict_add((s, f), roll, p1 * p2)

        rolls = self._roll_skill_aux(roll, {(0, 0): 1.0}, skill_max_roll, skill_margin, skill_fail_at, skill_continue_under, skill_stop_at)

        result = {}
        for (success, fail), p in rolls.items():
            self.dict_add(success, result, p)
        return result

    def _roll_skill_aux(self, roll: dict[(int, int), float], current: dict[(int, int), float],
                        roll_left: int,
                        skill_margin: int,
                        skill_fail_at: int,
                        skill_continue_under: int,
                        skill_stop_at: int) -> dict[(int, int), float]:
        if roll_left == 0:
            return current

        cummul = {}

        for (s1, f1), p1 in current.items():
            stop = f1 >= skill_fail_at
            stop |= s1 >= skill_stop_at
            stop |= f1 + skill_margin >= skill_fail_at and s1 >= skill_continue_under
            if stop:
                success = s1
                fail = f1
                p = p1
                self.dict_add((success, fail), cummul, p)
            else:
                for (s2, f2), p2 in roll.items():
                    success, fail = self.level_fail(s1 + s2, f1 + f2, skill_fail_at)
                    p = p1 * p2
                    self.dict_add((success, fail), cummul, p)
        return self._roll_skill_aux(roll, cummul, roll_left - 1, skill_margin, skill_fail_at, skill_continue_under, skill_stop_at)

    def de(self, nb_die: int, die: list) -> dict[tuple[int, ...], float]:
        dice = die.copy()
        dice_proba = self.compute_dice_probabilities(dice)
        dice_effect_nb = len(die[0])
        result = {(0,) * dice_effect_nb: 1.0}
        for i in range(0, nb_die):
            new_result = {}
            for r1, p1 in result.items():
                for r2, p2 in dice_proba.items():
                    r = tuple(map(operator.add, r1, r2))
                    self.dict_add(r, new_result, p1 * p2)
            result = new_result
        return result

    @staticmethod
    def compute_dice_probabilities(result: list[list[int]]) -> dict[list[int], float]:
        proba = {}
        nb_face = len(result)
        for i in range(0, nb_face):
            Proba.dict_add(result[i], proba, 1.0 / nb_face)
        return proba

    @staticmethod
    def display_proba(proba: dict) -> str:
        s = "Roll: \n"
        for r, p in proba.items():
            s += Proba.print_bar(r, p)
        return s

    @staticmethod
    def display_at_least(proba: dict) -> str:
        s = "At least: \n"
        at_leat = 1.0
        for r, p in proba.items():
            s += Proba.print_bar(r, at_leat)
            at_leat -= p
        return s

    @staticmethod
    def print_bar(v: int, p: float) -> str:
        p = p * 100
        prefix_v = ' ' if v < 10 else ''
        prefix_p = '  ' if p < 10 else ' ' if p < 100 else ''
        bar = "x" * int(p * 2)
        if p > 0.01:
            return '{}{}: {}{:.2f}%  {}\n'.format(prefix_v, v, prefix_p, p, bar)
        return ""

    @staticmethod
    def compute_average(proba: dict[int, float]) -> float:
        average = 0
        for success, p in proba.items():
            average += success * p
        return average
import operator
import collections

# fight effect  (damage, shield remove, blue dice remove, black dice remove)
fight_at_empty = (0, 0, 0, 0)
fight_1d = (1, 0, 0, 0)
fight_2d = (2, 0, 0, 0)
fight_3d = (3, 0, 0, 0)
# deffence effect (shield, cancel)
fight_def_empty = (0, 0)
fight_1s = (1, 0)
fight_2s = (2, 0)
fight_es = (0, 1)


def d_skill_w(spe: int) -> list[tuple]:
    return [(0,), (0,), (1,), (1,), (1,), (spe,)]


def d_skill_b(spe: int) -> list[tuple]:
    return [(0,), (0,), (0,), (1,), (1,), (spe,)]


def d_fight_r(spe: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
    return [fight_1d, fight_2d, spe]


def d_fight_y(spe: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
    return [fight_at_empty, fight_1d, fight_2d, fight_3d, fight_3d, spe]


def d_fight_blue(spe: tuple[int, int]) -> list[tuple[int, int]]:
    return [fight_def_empty, fight_def_empty, fight_1s, fight_1s, fight_2s, spe]


def d_fight_black(spe: tuple[int, int]) -> list[tuple[int, int]]:
    return [fight_def_empty, fight_def_empty, fight_def_empty, fight_2s, fight_es, spe]


def dict_add(key, dicti, value):
    dicti[key] = (dicti[key] if key in dicti else 0) + value


def level_fail(success: int, fail: int, skill_fail_at: int) -> (int, int):
    f = fail
    s = success
    if fail >= skill_fail_at:
        f = skill_fail_at
        s = 0
    return s, f


def roll_fight(fight_flat: tuple[int, int, int, int],
              fight_nb_r: int, fight_r: list[tuple[int, int, int, int]],
              fight_nb_y: int, fight_y: list[tuple[int, int, int, int]],
              fight_nb_blue: int, fight_blue: list[tuple[int, int]],
              fight_nb_black: int, fight_black: list[tuple[int, int]]) -> dict[int, float]:
    cummul_damage = {fight_flat: 1.0}
    r_roll = de(fight_nb_r, fight_r)
    y_roll = de(fight_nb_y, fight_y)
    cummul_damage = fight_cummul(cummul_damage, r_roll)
    cummul_damage = fight_cummul(cummul_damage, y_roll)

    result = {}
    for (damage_roll, p_a) in cummul_damage.items():
        damage, shield_red, blue_dice_red, black_dice_red = damage_roll
        cummul_defense = {fight_def_empty: 1.0}
        nb_blue = fight_nb_blue - blue_dice_red
        nb_black = fight_nb_black - black_dice_red
        if nb_blue > 0:
            blue_roll = de(nb_blue, fight_blue)
            cummul_defense = fight_cummul(cummul_defense, blue_roll)
        if nb_black > 0:
            black_roll = de(nb_black, fight_black)
            cummul_defense = fight_cummul(cummul_defense, black_roll)
        for (defence_roll, p_d) in cummul_defense.items():
            damage_red, cancel = defence_roll
            total_damage = 0 if cancel > 0 else max((damage - max(0, damage_red - shield_red)), 0)
            dict_add(total_damage, result, p_a * p_d)
    return collections.OrderedDict(sorted(result.items()))


def fight_cummul(result: dict[tuple[int, ...], float], roll: dict[tuple[int, ...], float]) -> dict[tuple[int, ...], float]:
    cummul = {}
    for d_c, pc in result.items():
        for d_r, pr in roll.items():
            dict_add(tuple(map(operator.add, d_c, d_r)), cummul, pc * pr)
    return cummul


def roll_skill(skill_nb_w: int, skill_w: list[tuple[int]],
              skill_nb_b: int, skill_b: list[tuple[int]],
              skill_max_roll: int,
              skill_margin: int,
              skill_fail_at: int,
              skill_stop_at: int) -> dict[int, float]:
    roll = {}
    w_roll = de(skill_nb_w, skill_w)
    b_roll = de(skill_nb_b, skill_b)
    for success, p1 in w_roll.items():
        for fail, p2 in b_roll.items():
            s, f = level_fail(success[0], fail[0], skill_fail_at)
            dict_add((s, f), roll, p1 * p2)

    rolls = roll_skill_aux(roll, {(0, 0): 1.0}, skill_max_roll, skill_margin, skill_fail_at, skill_stop_at)

    result = {}
    for (success, fail), p in rolls.items():
        dict_add(success, result, p)
    return result


def roll_skill_aux(roll: dict[(int, int), float], current: dict[(int, int), float],
                  roll_left: int,
                  skill_margin: int,
                  skill_fail_at: int,
                  skill_stop_at: int) -> dict[(int, int), float]:
    if roll_left == 0:
        return current

    cummul = {}

    for (s1, f1), p1 in current.items():
        if f1 + skill_margin >= skill_fail_at or s1 >= skill_stop_at:
            success = s1
            fail = f1
            p = p1
            dict_add((success, fail), cummul, p)
        else:
            for (s2, f2), p2 in roll.items():
                success, fail = level_fail(s1 + s2, f1 + f2, skill_fail_at)
                p = p1*p2
                dict_add((success, fail), cummul, p)
    return roll_skill_aux(roll, cummul, roll_left - 1, skill_margin, skill_fail_at, skill_stop_at)


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
    nb_face = len(result)
    for i in range(0, nb_face):
        dict_add(result[i], proba, 1.0 / nb_face)
    return proba


def display_proba(proba: dict) -> str:
    s = "Roll: \n"
    for r, p in proba.items():
        s += print_bar(r, p)
    return s


def display_at_least(proba: dict) -> str:
    s = "At least: \n"
    at_leat = 1.0
    for r, p in proba.items():
        s += print_bar(r, at_leat)
        at_leat -= p
    return s


def print_bar(v: int, p: float) -> str:
    p = p * 100
    prefix_v = ' ' if v < 10 else ''
    prefix_p = '  ' if p < 10 else ' ' if p < 100 else ''
    bar = "x" * int(p * 2)
    if p > 0.01:
        return '{}{}: {}{:.2f}%  {}\n'.format(prefix_v, v, prefix_p, p, bar)
    return ""


def compute_average(proba: dict[int, float]) -> float:
    average = 0
    for success, p in proba.items():
        average += success*p
    return average
