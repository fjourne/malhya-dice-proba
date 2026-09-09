from proba import Proba

proba = Proba()
# SKILL
skill_nb_w = 2
skill_nb_b = 2
skill_fail_at = 2
skill_continue_under=0
skill_stop_at = 5
skill_margin = 1
# skill effect success / fail
skill_w_spe = 1
skill_b_spe = 0
skill_max_roll = 25

skill_roll = proba.roll_skill(skill_nb_w, proba.d_skill_w(skill_w_spe),
                              skill_nb_b, proba.d_skill_b(skill_b_spe),
                              skill_max_roll,
                              skill_margin,
                              skill_fail_at,
                              skill_continue_under,
                              skill_stop_at)
print("Skill average : {}".format(proba.compute_average(skill_roll)))
print(proba.display_at_least(skill_roll))
print(proba.display_proba(skill_roll))
