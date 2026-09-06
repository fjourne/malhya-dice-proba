from proba import *

# SKILL
skill_nb_w = 2
skill_nb_b = 2
skill_fail_at = 2
skill_stop_at = 5
skill_margin = 0
# skill effect success / fail
skill_w_spe = 1
skill_b_spe = 0
skill_max_roll = 25

skill_roll = roll_skill(skill_nb_w, d_skill_w(skill_w_spe),
                       skill_nb_b, d_skill_b(skill_b_spe),
                       skill_max_roll,
                       skill_margin,
                       skill_fail_at,
                       skill_stop_at)
print("Skill average : {}".format(compute_average(skill_roll)))
print(display_at_least(skill_roll))
print(display_proba(skill_roll))
